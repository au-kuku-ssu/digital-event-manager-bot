package org.ssu.team2.test.pages;

import com.codeborne.selenide.SelenideElement;
import io.qameta.allure.Step;

import java.time.Duration;

import static com.codeborne.selenide.Condition.visible;
import static com.codeborne.selenide.Selenide.$x;

public class MainChatTelegramPage {
    private final SelenideElement inputFindChat = $x("//input[@id='telegram-search-input' or @class='input-field-input is-empty input-search-input with-focus-effect']")
        .as("Поле поиска чатов");
    private final SelenideElement findChat = $x("//div[@class='search-section']//div[@class='info' or @class='row no-wrap row-with-padding row-clickable hover-effect rp chatlist-chat chatlist-chat-abitbigger']").as("Первый найденный чат");

    @Step("Найти чат по тегу '{tag}'")
    public void findByTag(String tag){
        inputFindChat.shouldBe(visible, Duration.ofSeconds(120)).clear();
        inputFindChat.sendKeys(tag);
        findChat.shouldBe(visible).click();
    }
}
