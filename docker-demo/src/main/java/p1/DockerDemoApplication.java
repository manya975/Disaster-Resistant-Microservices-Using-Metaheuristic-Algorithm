package p1;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@SpringBootApplication
@RestController
public class DockerDemoApplication {

    @GetMapping("/test-docker")
    public String generate() {
       return "This is docker hub";
}

    public static void main(String[] args) {
        SpringApplication.run(DockerDemoApplication.class, args);
    }
}
