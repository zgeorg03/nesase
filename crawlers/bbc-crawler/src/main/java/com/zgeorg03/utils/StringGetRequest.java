package com.zgeorg03.utils;


import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.concurrent.Callable;

import static org.apache.http.protocol.HTTP.USER_AGENT;

public class StringGetRequest implements Callable<String>{
    private static final Logger logger = LoggerFactory.getLogger(StringGetRequest.class);
    private final CloseableHttpClient client;
    private final HttpGet request;

    public StringGetRequest(String url, CloseableHttpClient client, int seconds) {
        this.client = client;
        this.request = new HttpGet(url);
        request.addHeader("User-Agent", USER_AGENT);
        request.setConfig(RequestConfig.custom()
                .setConnectTimeout(seconds)
                .setConnectionRequestTimeout(seconds)
                .build()
        );
    }

    @Override
    public String call() throws Exception {
        CloseableHttpResponse response = client.execute(request);

        logger.info("Response Code : " + response.getStatusLine().getStatusCode());

        BufferedReader rd = new BufferedReader( new InputStreamReader(response.getEntity().getContent()));
        StringBuffer result = new StringBuffer();
        String line = "";
        while ((line = rd.readLine()) != null) {
            result.append(line);
        }
        rd.close();
        response.close();
        return result.toString();
    }
}
