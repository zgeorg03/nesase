package com.zgeorg03;

import com.zgeorg03.crawlers.BBCPuller;
import com.zgeorg03.crawlers.NewsFeedPuller;
import org.apache.http.HttpHost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.impl.conn.DefaultProxyRoutePlanner;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class App {


    public static void main(String args[]) throws Exception {

        String memory = "./log";
        String proxyHost = "http://proxy.cs.ucy.ac.cy";
        int proxyPort = 8008;
        if(args.length==1){
            memory = args[0];
        }else if(args.length==3){
            memory = args[0];
            proxyHost = args[1];
            proxyPort = Integer.parseInt(args[2]);
        }
        int maxThreads = 16;
        int interval = 300; //Seconds

        final HashesLoader hashesLoader = new HashesLoader(memory);

        final AppendOnlyLogger appendOnlyLogger = new AppendOnlyLogger(memory);

        final CloseableHttpClient client;

        HttpHost proxy = new HttpHost(proxyHost,proxyPort, HttpHost.DEFAULT_SCHEME_NAME);

        if(args.length!=3)
            client= HttpClients.createDefault();
        else
            client= HttpClients.custom()
                    .setRoutePlanner(new DefaultProxyRoutePlanner(proxy)).build();

        final ExecutorService executorService = Executors.newFixedThreadPool(maxThreads);

        NewsArticleManager articleManager = new NewsArticleManager(interval, executorService, client,appendOnlyLogger, hashesLoader);

        NewsFeedPuller bbcWorldNewsCrawler = new BBCPuller("http://feeds.bbci.co.uk/news/world/rss.xml"
                ,interval,articleManager, client, "world",1);

        NewsFeedPuller topNewsCrawler = new BBCPuller("http://feeds.bbci.co.uk/news/rss.xml"
                ,interval,articleManager, client, "top",15);

        NewsFeedPuller business = new BBCPuller("http://feeds.bbci.co.uk/news/business/rss.xml"
                ,interval,articleManager, client, "business",30);

        NewsFeedPuller tech = new BBCPuller("http://feeds.bbci.co.uk/news/technology/rss.xml"
                ,interval,articleManager, client, "tech",45);

        NewsFeedPuller science = new BBCPuller("http://feeds.bbci.co.uk/news/science_and_environment/rss.xml"
                ,interval,articleManager, client, "science",60);

        final ExecutorService crawlers = Executors.newFixedThreadPool(5);
        crawlers.submit(bbcWorldNewsCrawler);
        crawlers.submit(topNewsCrawler);
        crawlers.submit(business);
        crawlers.submit(tech);
        crawlers.submit(science);

        //Run in main thread
        articleManager.run();


    }

}
