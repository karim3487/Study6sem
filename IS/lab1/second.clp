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
    (switch (ask_question "Это блюдо жарят (1) / варят (2) / запекают (3)? " 1 2 3)
        (case 1 then (assert (cooking_method fry)))
        (case 2 then (assert (cooking_method brew)))
        (case 3 then 
            (assert (cooking_method bake))
            (bind ?*answer* "Запеченная курица")
        )
    )
)

(defrule question-2
    (declare (salience 3))
    (cooking_method fry)
    =>
    (switch (ask_question "В составе блюда есть мука (1) / нет муки (2)? " 1 2)
        (case 1 then 
           (assert (is_flour_product))
           (bind ?*answer* Пирожки)
        )
        (case 2 then 
            (assert (is_not_flour_pruduct))
            (bind ?*answer* Котлеты)
        )
    )
)

(defrule question-3
    (declare (salience 3))
    (cooking_method brew)
    =>
    (switch (ask_question "В составе блюда есть мука (1) / нет муки (2)? " 1 2)
        (case 1 then (assert (is_flour_product)))
        (case 2 then (assert (is_not_flour_product)))
    )
)

(defrule question-4
    (declare (salience 2))
    (is_not_flour_product)
    =>
    (switch (ask_question "В это блюдо добавляют несколько продуктов (1) / нет (2)?  " 1 2)
        (case 2 then
            (assert (single_food_dish))
            (bind ?*answer* Вареная картошка)
        )
        (case 1 then
            (assert (multy_food_dish))
            (bind ?*answer* Cуп)
        )
    )
)

(defrule question-5
    (declare (salience 2))
    (is_flour_dish)
    =>
    (switch (ask_question "У этого блюда есть мясная начинка (1) / нет (2)? " 1 2)
        (case 1 then
            (assert (with_meat_filling))
            (bind ?*answer* Пельмени)
        )
        (case 2 then
            (assert (without_meat_filling))
            (bind ?*answer* Макароны)
        )
    )
)
; ВЫВОД ОТВЕТА

(defrule output_answer
    (declare (salience 1))
    
    =>
    (printout t crlf "Это " ?*answer* "!!!" crlf)
)

