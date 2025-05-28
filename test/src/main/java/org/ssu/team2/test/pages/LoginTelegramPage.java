package org.ssu.team2.test.pages;

import com.codeborne.selenide.Condition;
import com.codeborne.selenide.SelenideElement;
import io.qameta.allure.Step;
import org.openqa.selenium.Keys;

import java.time.Duration;
import java.util.Objects;

import static com.codeborne.selenide.Condition.*;
import static com.codeborne.selenide.Selenide.$x;
import static com.codeborne.selenide.Selenide.sleep;

public class LoginTelegramPage {

    private final SelenideElement numberInput= $x("//*[@id='sign-in-phone-number' or @class='input-field input-field-phone']")
        .as("Поле ввода телефона");
    private final SelenideElement keepMeCheckBox = $x("//input[@id='sign-in-keep-session']").as("Чекбокс \"Запомнить меня\"");
    private final SelenideElement codeInput = $x("//input[@id='sign-in-code' or @class='input-field-input is-empty']")
        .as("Поле ввода кода");
//    private final SelenideElement buttonContinue = $x("//*[text()='Далее']").as("Кнопка Далее");
    private final SelenideElement inputPassword = $x("//input[@name='notsearch_password' or @type='password' and not(@class='stealthy')]")
        .as("Поле ввода пароля");
    private final SelenideElement submitButton = $x("//*[@type='submit' or text()='Далее']");

    @Step("Ввести номер телефона '{number}'")
    public LoginTelegramPage inputNumber(String number){
        sleep(2000);
        if(Objects.requireNonNull(numberInput.shouldBe(visible, Duration.ofSeconds(20)).getAttribute("id")).equals("sign-in-phone-number")){
            numberInput.sendKeys(number.substring(2));
        }else {
            numberInput.$x("./div[@inputmode='decimal']").clear();
            numberInput.$x("./div[@inputmode='decimal']").sendKeys(Keys.chord(Keys.CONTROL,"a") + number);
        }
        sleep(1000L);
        if (keepMeCheckBox.is(exist) && keepMeCheckBox.is(Condition.selected)){
            keepMeCheckBox.parent().click();
        }

        if (submitButton.getTagName().equals("span")){
            submitButton.parent().click();
        }else {
            submitButton.click();
        }
        return this;
    }

    //код приходит вам в тг, вводим ручками, по другому никак
    @Step("Ввести код")
    public LoginTelegramPage inputCode(){
     codeInput.shouldBe(visible, Duration.ofSeconds(30));
     codeInput.shouldNotBe(visible, Duration.ofSeconds(30));
     return this;
    }

    @Step("Ввести пароль")
    public LoginTelegramPage inputPassword(String password){
        inputPassword.shouldBe(editable, Duration.ofSeconds(15)).sendKeys(password);
        if(submitButton.shouldBe(visible).getTagName().equals("span")){
            submitButton.parent().click();
        } else {
            submitButton.click();
        }
        return  this;
    }
}
