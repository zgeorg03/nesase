package com.zgeorg03.crawlers;

import com.zgeorg03.NewsArticleManager;
import com.zgeorg03.exceptions.ArticleAlreadyExistsException;
import com.zgeorg03.models.MissingContentRecord;
import org.apache.commons.codec.digest.DigestUtils;
import org.apache.http.impl.client.CloseableHttpClient;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.parser.Parser;
import org.jsoup.select.Elements;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.text.DateFormat;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class BBCPuller extends NewsFeedPuller {

    private final Logger logger = LoggerFactory.getLogger(BBCPuller.class);

    DateFormat fmt = new SimpleDateFormat("E, dd MMM yyyy HH:mm:ss z");

    private final String feed;


    public BBCPuller(String rssPath, int interval, NewsArticleManager manager, CloseableHttpClient client, String feed, int initialSleep) {
        super(rssPath, interval,initialSleep, manager, client);
        this.feed = feed;
    }

    @Override
    public void pullNewsHeaders(String result) {

        //Parse the xml file returned
        Document doc = Jsoup.parse(result,"", Parser.xmlParser());

        //Select all items
        Elements elements = doc.select("rss channel item");

        // For each item
        for(Element element : elements){
            String title = element.select("title").first().text();
            String strDate = element.select("pubDate").first().text();
            String hash= DigestUtils.md5Hex(title+strDate);

            try {
                Date date = fmt.parse(strDate);

                String link = element.select("link").first().text();

                MissingContentRecord contentRecord = new MissingContentRecord(hash, link, title, feed, date);

                manager.addTask(hash,contentRecord);
                countNew++;

            }catch (ParseException e){
                logger.error(e.getLocalizedMessage());
                countFailed++;

            } catch (ArticleAlreadyExistsException e) {
                countExisting++;

            }

        }

    }
}
