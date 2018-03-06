package com.zgeorg03.models;

import java.util.Date;

public class MissingContentRecord {
    private final String hash;
    private final String link;
    private final String title;
    private final String feed;
    private final Date date;

    public MissingContentRecord(String hash, String link, String title, String feed, Date date) {
        this.hash = hash;
        this.link = link;
        this.title = title;
        this.feed = feed;
        this.date = date;
    }

    public String getLink() {
        return link;
    }

    public Date getDate() {
        return date;
    }

    public String getTitle() {
        return title;
    }

    public String getFeed() {
        return feed;
    }

    @Override
    public String toString() {
        return "MissingContentRecord{" +
                "link='" + link + '\'' +
                ", title='" + title + '\'' +
                ", date=" + date +
                '}';
    }

    public String getHash() {
        return hash;
    }
}
