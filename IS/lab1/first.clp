; ПРОВЕРКА ВВОДА

(deffunction ask_question (?question $?allowed_values)
   (printout t ?question)
   (bind ?answer (read))
   (if (lexemep ?answer) 
       then (bind ?answer (lowcase ?answer)))
   (while (not (member$ ?answer ?allowed_values)) do
      (printout t crlf "Некорректный ввод данных, повторите попытку." crlf)
      (printout t crlf ?question)
      (bind ?answer (read))
      (if (lexemep ?answer) 
          then (bind ?answer (lowcase ?answer))))
    ?answer
)

; ЗАДАНИЕ ПО ВАРИАНТУ 
; ЛОГИКА ПРОГРАММЫ

(defglobal ?*answer* = nil)

(defrule question-1
    (declare (salience 4))
    =>
    (switch (ask_question "Игра в мяч происходит в помещении (1) / на открытой площадке (2) / в воде (3)? " 1 2 3)
        (case 1 then (assert (game_in room)))
        (case 2 then (assert (game_in outer_playground)))
        (case 3 then 
            (assert (game_in water))
            (bind ?*answer* "Водное поло")
        )
    )
)

(defrule question-2
    (declare (salience 3))
    (game_in room)
    =>
    (switch (ask_question "Игра командная (1) / не командная (2)? " 1 2)
        (case 1 then 
           (assert (game_type team))
           (bind ?*answer* Баскетбол)
        )
        (case 2 then 
            (assert (game_type not_team))
            (bind ?*answer* Сквош)
        )
    )
)

(defrule question-3
    (declare (salience 3))
    (game_in outer_playground)
    =>
    (switch (ask_question "Играют с вратарями (1) / без вратарей (2)? " 1 2)
        (case 1 then (assert (game_with goalkeepers)))
        (case 2 then (assert (game_without goalkeepers)))
    )
)

(defrule question-4
    (declare (salience 2))
    (game_with goalkeepers)
    =>
    (switch (ask_question "У игроков есть доп. инвентарь (1) / нет инвентаря (2)? " 1 2)
        (case 1 then
            (assert (game_with inventory))
            (bind ?*answer* Футбол)
        )
        (case 2 then
            (assert (game_without inventory))
            (bind ?*answer* Хоккей на траве)
        )
    )
)

(defrule question-5
    (declare (salience 2))
    (game_without goalkeepers)
    =>
    (switch (ask_question "У игроков есть доп. инвентарь (1) / нет инвентаря (2)? " 1 2)
        (case 1 then
            (assert (game_with inventory))
            (bind ?*answer* Бейсбол)
        )
        (case 2 then
            (assert (game_without inventory))
            (bind ?*answer* Пляжный волейбол)
        )
    )
)
; ВЫВОД ОТВЕТА

(defrule output_answer
    (declare (salience 1))
    
    =>
    (printout t crlf "Это " ?*answer* "!!!" crlf)
)

