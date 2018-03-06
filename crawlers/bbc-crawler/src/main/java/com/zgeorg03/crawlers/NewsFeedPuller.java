package com.zgeorg03.crawlers;

import com.zgeorg03.NewsArticleManager;
import com.zgeorg03.utils.StringGetRequest;
import org.apache.http.impl.client.CloseableHttpClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.TimeUnit;

public abstract class NewsFeedPuller implements Runnable{
    private static final Logger logger = LoggerFactory.getLogger(NewsFeedPuller.class);
    protected final String rssPath;
    protected final int interval;
    protected final NewsArticleManager manager;
    protected final CloseableHttpClient client;

    private int initialSleep = 1;

    protected int countFailed=0;
    protected int countExisting=0;
    protected int countNew=0;

    public NewsFeedPuller(String rssPath, int interval,int initialSleep, NewsArticleManager manager, CloseableHttpClient client) {
        this.rssPath = rssPath;
        this.interval = interval;
        this.manager = manager;
        this.client = client;
        this.initialSleep = initialSleep;
    }

    @Override
    public void run() {
        try { TimeUnit.SECONDS.sleep(initialSleep); } catch (InterruptedException e) { logger.error(e.getLocalizedMessage()); }
        while(true) {
            logger.info("Pulling news feed from:" + rssPath);

            try {
                String xml = new StringGetRequest(rssPath,client,5000).call();
                countExisting = 0;
                countNew = 0;
                countFailed = 0;
                pullNewsHeaders(xml);
                logger.info("New:"+countNew+"\t"+"Exist:"+countExisting+"\t"+"Fail:"+countFailed);

            } catch (Exception e) {
                logger.error(e.getLocalizedMessage());
            }

            try { TimeUnit.SECONDS.sleep(interval); } catch (InterruptedException e) { logger.error(e.getLocalizedMessage()); }
        }
    }

    public abstract void pullNewsHeaders(String result);
}
