package com.zgeorg03;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.Set;
import java.util.TreeSet;

public class HashesLoader {
    private final Logger logger = LoggerFactory.getLogger(HashesLoader.class);
    private Set<String> hashes = new TreeSet<>();

    private final long start = System.currentTimeMillis();
    private long end;
    private int count;

    public HashesLoader(String path) throws IOException {

        File file = Paths.get(path).toFile();

        if(!file.exists())
            return;

        loadHashes(file);
        logger.info(stats());
    }

    public void loadHashes(File file) throws IOException {
        BufferedReader bf = new BufferedReader(new FileReader(file));
        String line = "";
        while((line=bf.readLine())!=null){
            if(line.startsWith(","))
                continue;

            line = line.substring(9,41);

            if(!hashes.add(line)) {
                logger.info("Conflicting hash found:" + line);
                continue;
            }
            count++;
        }
        end = System.currentTimeMillis();
    }
    public String stats(){
        return "Took "+ (end-start)+" ms to load " +count+" hashes";
    }

    public boolean addNewHash(String hash){
        if(!hashes.add(hash)) {
            logger.info("Conflicting hash found:" + hash);
            return false;
        }
        return true;
    }

    public boolean containsHash(String hash){
        return hashes.contains(hash);
    }

}
