package org.ssu.team2.test.helper;


import org.aeonbits.owner.Config;
import org.aeonbits.owner.ConfigFactory;

@Config.LoadPolicy(Config.LoadType.MERGE)
@Config.Sources({
    "classpath:generaltest.properties"
})
public interface Props extends Config {

    Props props = ConfigFactory.create(Props.class);

    @Key("base.url")
    String baseUrl();

    @Key("bot.username")
    String botUsername();

    @Key("number.phone")
    String numberPhone();

    @Key("password")
    String password();
}
