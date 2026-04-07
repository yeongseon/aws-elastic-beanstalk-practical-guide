package com.example.ebguide.controller;

import java.time.OffsetDateTime;
import java.util.Map;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class InfoController {

    @Value("${spring.application.name:ebguide}")
    private String applicationName;

    @Value("${APP_NAME:eb-java-guide}")
    private String elasticBeanstalkApplicationName;

    @GetMapping("/info")
    public Map<String, String> info() {
        return Map.of(
                "application", applicationName,
                "elasticBeanstalkApplication", elasticBeanstalkApplicationName,
                "timestamp", OffsetDateTime.now().toString()
        );
    }
}
