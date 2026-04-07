package com.example.guide.controller;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class DemoController {

    private static final List<String> SAFE_KEYS = List.of("ENV_NAME", "APP_VERSION", "LOG_LEVEL", "AWS_REGION");

    @GetMapping("/")
    public Map<String, Object> index() {
        return Map.of(
                "application", "aws-eb-java-reference",
                "status", "running",
                "health", "/health",
                "info", "/info",
                "environment", "/demo/env"
        );
    }

    @GetMapping("/demo/env")
    public Map<String, Object> demoEnvironment() {
        Map<String, String> values = new LinkedHashMap<>();
        for (String key : SAFE_KEYS) {
            values.put(key, System.getenv().getOrDefault(key, "not-set"));
        }

        return Map.of(
                "environmentProperties", values,
                "port", System.getenv().getOrDefault("PORT", "5000")
        );
    }
}
