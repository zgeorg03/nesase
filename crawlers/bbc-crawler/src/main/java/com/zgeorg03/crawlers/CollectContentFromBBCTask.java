package com.zgeorg03.crawlers;

import com.zgeorg03.utils.StringGetRequest;
import com.zgeorg03.models.CompleteArticle;
import com.zgeorg03.models.MissingContentRecord;
import org.apache.http.impl.client.CloseableHttpClient;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Callable;

public class CollectContentFromBBCTask implements Callable<CompleteArticle>{
    private final Logger logger  = LoggerFactory.getLogger(CollectContentFromBBCTask.class);


    protected final CloseableHttpClient client;
    protected final String url;
    protected final MissingContentRecord record;

    public CollectContentFromBBCTask(CloseableHttpClient client, String url, MissingContentRecord record) {
        this.client = client;
        this.url = url;
        this.record = record;
    }

    @Override
    public CompleteArticle call() throws Exception {
        String html = new StringGetRequest(url,client,15000).call();
        Document document = Jsoup.parse(html);
        List<String> tags = new LinkedList<>();
        Elements tagsElements = document.select("li.tags-list__tags");
        for(Element el : tagsElements){
           String tag = el.text();
           tags.add(tag);
        }

        logger.info("Trying: "+url);
        Element content = document.selectFirst("div.story-body__inner");

        //Try for media
        if(content==null){
            content = document.selectFirst("div.vxp-media__body");
        }

        //Try athletics
        if(content==null){
            content = document.selectFirst("div#story-body");
        }
        //Try tennis
        if(content==null){
            content = document.selectFirst("div.gel-body-copy.sp-c-media-collection_body-copy");
        }

        Elements paragraphs = content.select("h1,p,h2");
        StringBuilder stringBuilder = new StringBuilder();
        for(Element p: paragraphs){
            stringBuilder.append(p.text());
            if(p.is("p"))
                stringBuilder.append(" ");
            if(p.is("h2"))
                stringBuilder.append("\n");
        }
        String text = stringBuilder.toString();

        return new CompleteArticle(record.getHash(), record.getTitle(),"bbc", record.getFeed(), url,text,record.getDate(),tags);
    }
}
