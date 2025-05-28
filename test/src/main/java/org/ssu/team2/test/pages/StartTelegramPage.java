package org.ssu.team2.test.pages;

import com.codeborne.selenide.SelenideElement;
import io.qameta.allure.Step;

import java.time.Duration;

import static com.codeborne.selenide.Condition.visible;
import static com.codeborne.selenide.Selenide.$x;

public class StartTelegramPage {
    private final SelenideElement buttonContinueInRussian = $x("//*[text()='Продолжить на русском']").as("Кнопка продолжить на русском");
    private final SelenideElement startByPhone = $x("//*[text()='Вход по номеру телефона']")
        .as("Кнопка \"Вход по номеру телефона\"");

    @Step("Нажать кнопку старт по телефону")
    public void startByPhone(){
        clickElement(buttonContinueInRussian);
        clickElement(startByPhone);
    }

    @Step("Кликнуть по элементу '{element}'")
    private void clickElement(SelenideElement element){
        element.shouldBe(visible, Duration.ofSeconds(20));
        if(element.getTagName().equals("span")){
            element.parent().click();
        } else {
            element.click();
        }
    }
}
