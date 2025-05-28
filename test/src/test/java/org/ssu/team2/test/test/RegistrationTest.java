package org.ssu.team2.test.test;

import com.codeborne.selenide.Selenide;
import org.junit.jupiter.api.Test;
import org.ssu.team2.test.hooks.WebHooks;
import org.ssu.team2.test.pages.ChatTelegramPage;
import org.ssu.team2.test.pages.LoginTelegramPage;
import org.ssu.team2.test.pages.MainChatTelegramPage;
import org.ssu.team2.test.pages.StartTelegramPage;

public class RegistrationTest extends WebHooks {
    @Test
    public void registration_test(){

        new StartTelegramPage()
            .startByPhone();

        new LoginTelegramPage()
            .inputNumber(props.numberPhone())
            .inputCode()
            .inputPassword(props.password());

        new MainChatTelegramPage().findByTag(props.botUsername());

        new ChatTelegramPage().startBot()
            .clickButtonInChat("Русский ")
            .clickButtonInChat(" Регистрация участника")
            .clickButtonInChat("Мои личные данные")
            .clickButtonInChat("Пройти регистрацию")
            .sendMessage("Фамилия Имя Отчествович")
            .sendMessage("89992119999")
            .sendMessage("asdas@mail.ru")
            .deleteHistory();
    }
}
