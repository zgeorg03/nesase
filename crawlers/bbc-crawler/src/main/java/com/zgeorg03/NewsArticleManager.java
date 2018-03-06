package com.zgeorg03;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.zgeorg03.crawlers.CollectContentFromBBCTask;
import com.zgeorg03.exceptions.ArticleAlreadyExistsException;
import com.zgeorg03.models.CompleteArticle;
import com.zgeorg03.models.MissingContentRecord;
import org.apache.http.impl.client.CloseableHttpClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Queue;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.*;

public class NewsArticleManager implements Runnable {

    private static final Logger logger = LoggerFactory.getLogger(NewsArticleManager.class);

    private Queue<MissingContentRecord> tasks = new ConcurrentLinkedQueue<>();

    //Store the ones we've seen
    private Set<String> cache = new TreeSet<>();

    private final int sleep;

    private final ExecutorCompletionService<CompleteArticle> completionService;
    private final CloseableHttpClient httpClient;

    private final AppendOnlyLogger appendOnlyLogger;
    private final HashesLoader hashesLoader;

    private final Gson gson = new GsonBuilder().create();

    public NewsArticleManager(int sleep, ExecutorService service, CloseableHttpClient httpClient, AppendOnlyLogger appendOnlyLogger, HashesLoader hashesLoader) throws IOException {
        this.sleep = sleep;
        this.completionService = new ExecutorCompletionService<>(service);
        this.httpClient = httpClient;
        this.appendOnlyLogger = appendOnlyLogger;
        this.hashesLoader = hashesLoader;
    }

    public void addTask(String key, MissingContentRecord record) throws ArticleAlreadyExistsException {

        if(cache.contains(key))
            throw new ArticleAlreadyExistsException(key);

        if(hashesLoader.containsHash(key))
            throw new ArticleAlreadyExistsException(key);

        cache.add(key);
        tasks.add(record);

    }

    @Override
    public String toString() {
        return "NewsArticleManager{" +
                "tasks=" + tasks +
                '}';
    }

    @Override
    public void run() {

        int actualSleep = 1;
        while (true){

            int countSubmitted = 0;
            while(!tasks.isEmpty()) {
                MissingContentRecord record = tasks.poll();
                completionService.submit(new CollectContentFromBBCTask(httpClient,record.getLink(), record));
                countSubmitted++;
            }
            logger.info("Submitted "+countSubmitted+" tasks to collect content");

            Future<CompleteArticle> completedTaskFuture = completionService.poll();
            if (completedTaskFuture!=null){

                try {
                    CompleteArticle article = completedTaskFuture.get(60,TimeUnit.SECONDS);
                    appendOnlyLogger.appendTransaction(gson.toJson(article.toJson()));
                    hashesLoader.addNewHash(article.getHash());
                    cache.remove(article.getHash());
                } catch (InterruptedException e) {
                } catch (ExecutionException e) {
                    e.printStackTrace();
                    logger.error(e.getLocalizedMessage());
                } catch (TimeoutException e) {
                    logger.info("Waited for 60 seconds and nobody finished...");
                }
                actualSleep=1;
            }

            logger.info("Putting into sleep for "+actualSleep+" seconds");

            //Sleep a bit
            try { TimeUnit.SECONDS.sleep(actualSleep); } catch (InterruptedException e) { e.printStackTrace(); }

            if(actualSleep<sleep)
                actualSleep*=2;
        }

    }
}
