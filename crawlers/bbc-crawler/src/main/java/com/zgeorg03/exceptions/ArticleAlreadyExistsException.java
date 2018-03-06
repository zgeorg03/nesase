package com.zgeorg03.exceptions;

public class ArticleAlreadyExistsException extends Exception {
    public ArticleAlreadyExistsException(String key) {
        super("Article "+key+" already exists");
    }
}
