package com.zgeorg03;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.nio.file.Paths;

public class AppendOnlyLogger {
    private final Logger logger = LoggerFactory.getLogger(AppendOnlyLogger.class);
    private final File file;
    private final PrintWriter writer;

    public AppendOnlyLogger(String path) throws Exception {
        this.file = Paths.get(path).toFile();
        if(file.isDirectory())
            throw new Exception("Log must be a file");
        writer = new PrintWriter(new FileWriter(file,true));
    }

    public void appendTransaction(String json){
        logger.trace("Writing to log...");
        writer.write(json);
        writer.write("\n,\n");
        writer.flush();
    }
}
