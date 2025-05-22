package org.ssu.team2.test.pages;

import com.codeborne.selenide.Selenide;
import com.codeborne.selenide.SelenideElement;
import io.qameta.allure.Step;
import org.openqa.selenium.Keys;

import java.time.Duration;

import static com.codeborne.selenide.Condition.visible;
import static com.codeborne.selenide.Selenide.$x;
import static com.codeborne.selenide.Selenide.sleep;

public class ChatTelegramPage {
    private final SelenideElement startBButton = $x("//button[text()='СТАРТ']").as("Кнопка старта бота");
    private final SelenideElement messageInput = $x("//div[@id='editable-message-text']").as("Поле ввода сообщения");
    private final SelenideElement moreActionsButton = $x("//button[@aria-label='More actions']").as("Кнопка \"Больше опций\"");
    private final SelenideElement deleteChatButton = $x("//div[text()='Удалить чат']").as("Кнопка удалить чат");
    private final SelenideElement deleteChatButton2 = $x("//h3[text()='Удалить чат']/../..//button[text()='Удалить']").as("Кнопка удалить чат");


    private SelenideElement buttonInChat(String nameButton){
        return $x("//span[@class='inline-button-text' and text()='" + nameButton + "']/..").as("Кнопка " + nameButton + " в чате");
    }

    @Step("Включить чат-бот")
    public ChatTelegramPage startBot(){
        sleep(1000L);
        startBButton.shouldBe(visible, Duration.ofSeconds(20)).click();
        sleep(1000L);
        return this;
    }

    @Step("Ввести и отправить сообщение '{message}'")
    public ChatTelegramPage sendMessage(String message){
        messageInput.sendKeys(message + Keys.ENTER);
        return this;
    }

    @Step("Нажать кнопку '{nameButton}' в чате")
    public ChatTelegramPage clickButtonInChat(String nameButton){
        buttonInChat(nameButton).shouldBe(visible, Duration.ofSeconds(20)).click();
        return this;
    }

    @Step("Удалить историю чата")
    public ChatTelegramPage deleteHistory(){
        moreActionsButton.click();
        deleteChatButton.click();
        deleteChatButton2.click();
        return this;
    }
}
