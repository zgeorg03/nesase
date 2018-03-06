package com.zgeorg03.models;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.util.Date;
import java.util.List;

public class CompleteArticle {
    private final String hash;
    private final String title;
    private final String author;
    private final String feed;
    private final String link;
    private final String content;
    private final Date date;
    private final List<String> topics;

    @Override
    public String toString() {
        return "CompleteArticle{" +
                "hash='" + hash + '\'' +
                ", title='" + title + '\'' +
                ", author='" + author + '\'' +
                ", feed='" + feed + '\'' +
                ", link='" + link + '\'' +
                ", content='" + content + '\'' +
                ", date=" + date +
                ", topics=" + topics +
                '}';
    }

    public CompleteArticle(String hash, String title, String author, String feed, String link, String content, Date date, List<String> topics) {
        this.hash = hash;
        this.title = title;
        this.author = author;
        this.feed = feed;
        this.link = link;
        this.content = content;
        this.date = date;
        this.topics = topics;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getLink() {
        return link;
    }

    public String getContent() {
        return content;
    }

    public Date getDate() {
        return date;
    }

    public List<String> getTopics() {
        return topics;
    }

    public String getHash() {
        return hash;
    }

    public JsonObject toJson(){
        JsonObject object = new JsonObject();
        object.addProperty("hash",hash);
        object.addProperty("title",title);
        object.addProperty("author",author);
        object.addProperty("feed", feed);
        object.addProperty("link",link);
        object.addProperty("content",content);
        object.addProperty("date",date.getTime());
        JsonArray array = new JsonArray();
        topics.stream().forEach(x->array.add(x));
        object.add("topics",array);
        return object;
    }
}
