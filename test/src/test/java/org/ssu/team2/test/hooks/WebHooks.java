package org.ssu.team2.test.hooks;

import com.codeborne.selenide.Configuration;
import com.codeborne.selenide.Selenide;
import com.codeborne.selenide.WebDriverRunner;
import com.codeborne.selenide.logevents.SelenideLogger;
import io.qameta.allure.selenide.AllureSelenide;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.openqa.selenium.PageLoadStrategy;
import org.openqa.selenium.WebDriver;
import org.ssu.team2.test.helper.Props;

public class WebHooks {

    protected Props props = Props.props;

    @BeforeEach
    public void initBrowser() {
        Configuration.pageLoadStrategy = PageLoadStrategy.NORMAL.toString();
        Configuration.timeout = 15000;

        SelenideLogger.addListener("AllureSelenide",
            new AllureSelenide()
                .screenshots(true)
                .savePageSource(false));

        Selenide.open(props.baseUrl());
        WebDriver driver = WebDriverRunner.getWebDriver();
        driver.manage().window().maximize();


    }

    @AfterEach
    public void afterTest() {
        Selenide.closeWebDriver();
    }
}
