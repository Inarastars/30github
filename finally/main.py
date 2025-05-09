import random

quotes = [
    "Самый мудрый человек тот, кто знает, что он ничего не знает.",
    "Жизнь измеряется не числом вдохов, а моментами, захватывающими дух.",
    "Не бойся медлить, бойся остановиться.",
    "Будь собой, все остальные роли уже заняты.",
    "Мы получаем от жизни то, во что верим.",
    "Лучше зажечь свечу, чем проклинать темноту.",
    "Терпение — это не умение ждать, а умение сохранять хорошее настроение, пока ждёшь.",
    "Будущее зависит от того, что мы делаем в настоящем.",
    "Дорогу осилит идущий.",
    "Тот, кто хочет видеть радугу, должен пережить дождь.",
    "Ошибки — это доказательство того, что ты пытаешься.",
    "Не говори, что тебе не везёт, просто подумай, как ты используешь свои шансы.",
    "Иногда поражение – это всего лишь начало чего-то нового.",
    "Счастье — это не пункт назначения, а образ жизни.",
    "Если хочешь изменить мир — начни с себя.",
    "Лучший способ предсказать будущее — создать его.",
    "Когда ты перестанешь гнаться за неправильными вещами, ты начнёшь ловить правильные.",
    "Учись у вчера, живи сегодня, надейся на завтра.",
    "Если боишься — не делай, если делаешь — не бойся.",
    "Не позволяй малым неудачам сбить тебя с пути к большой цели.",
    "Мы живем так, как мыслям позволяем.",
    "Мудрость приходит с опытом, а опыт — с ошибками.",
    "Всегда стремись стать лучшей версией себя.",
    "Чтобы дойти до цели, нужно прежде всего идти.",
    "Все приходит вовремя для того, кто умеет ждать.",
    "Успех — это лестница, на которую не забраться, держа руки в карманах.",
    "Мысли глобально, действуй локально.",
    "Падая, учись подниматься.",
    "Если хочешь быть счастливым – будь им.",
    "Чем труднее борьба, тем славнее победа.",
    "Лучшая месть — это огромный успех.",
    "Не сравнивай свою главу первой с чьей-то десятой.",
    "Где нет борьбы, там нет и силы.",
    "Ты не можешь контролировать ветер, но можешь настроить паруса.",
    "Ты становишься тем, о чем думаешь весь день.",
    "Не бойся ошибаться, бойся ничего не делать.",
    "Величие начинается там, где заканчивается комфорт.",
    "Твой единственный соперник — ты вчерашний.",
    "Неудачи — это ступени к успеху.",
    "Чем больше ты стараешься, тем больше тебе везёт.",
    "Если хочешь идти быстро – иди один, если хочешь идти далеко – иди вместе.",
    "Твоя жизнь — результат твоих выборов.",
    "Не считай дни, а наполняй их смыслом.",
    "Только те, кто рискуют идти далеко, могут узнать, как далеко они могут зайти.",
    "Каждый человек — архитектор своего счастья.",
    "Лучше сделать и пожалеть, чем не сделать и всю жизнь думать, что мог бы.",
    "Сомнения убивают больше мечт, чем неудачи.",
    "Жизнь — это то, что с тобой происходит, пока ты строишь планы.",
    "Если мечтаешь — значит, можешь осуществить.",
    "Действие — ключ к любому успеху.",
    "Пока ты не сдаешься — ты не проиграл.",
    "Возможности не приходят сами – ты создаёшь их.",
    "Сильные люди создают своё будущее сами.",
    "Успех любит упорных.",
    "Перемены начинаются с одного шага.",
    "Ты либо управляешь своим днем, либо день управляет тобой.",
    "Никогда не поздно стать тем, кем мог бы стать.",
    "Если тебя сбили с ног – вставай и иди дальше.",
    "Не бойся идти медленно, бойся стоять на месте.",
    "Ты сильнее, чем думаешь.",
    "Кто хочет – ищет возможности, кто не хочет – ищет оправдания.",
    "Только упорство ведет к великим свершениям.",
    "Не бойся выходить за рамки.",
    "Трудности закаляют характер.",
    "Чудеса случаются, когда ты не сдаешься.",
    "Лучший способ начать – перестать говорить и начать делать.",
    "Когда ты хочешь сдаться – вспомни, ради чего ты начинал.",
    "Нет ничего невозможного.",
    "У каждого есть силы добиться своей цели.",
    "Пока ты веришь — у тебя есть шанс.",
    "Мечтай. Действуй. Достигай.",
    "Сначала ты работаешь на репутацию, потом она работает на тебя.",
    "Побеждает тот, кто верит в себя.",
    "Смелость – это начало победы.",
    "Жизнь – это не ожидание, а действие.",
    "Не важно, как медленно ты движешься, важно, что ты не останавливаешься.",
    "Лучше ошибиться, чем никогда не попробовать.",
    "Мир принадлежит тем, кто встает рано.",
    "Все великие дела начинались с малого.",
    "Кто не рискует – тот не пьет шампанского.",
    "Не позволяй страху мешать тебе двигаться вперед.",
    "Не откладывай на завтра то, что можешь сделать сегодня.",
    "Пока не попробуешь – не узнаешь.",
    "Каждая неудача приближает к успеху.",
    "Если ты упал — не задерживайся там.",
    "Делай сегодня то, за что завтра скажешь себе спасибо.",
    "Секрет успеха – в постоянстве.",
    "Живи так, чтобы не жалеть ни о чем.",
    "Главное – начать.",
    "Когда ты видишь цель, препятствия перестают существовать.",
    "Настоящая победа – это победа над собой.",
    "Пока есть желание – есть возможность.",
    "Не сдавайся, и всё получится.",
    "У каждого из нас есть время, вопрос в том, как мы его используем.",
    "Смелость начинается с первого шага.",
    "Улыбка – твое лучшее оружие.",
    "Ты создаешь свою реальность сам.",
    "Будь упорным – и мир уступит.",
    "Именно через трудности приходит успех.",
    "Жизнь любит тех, кто ее любит.",
]
print(random.choice(quotes))