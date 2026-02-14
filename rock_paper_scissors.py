import random

def game():
  print("Hello world!")
  # Список вариантов
  options = ["камень", "ножницы", "бумага"]
  
  print("==============================")
  print("==  Камень Ножницы Бумага  ==")
  print("==============================")
  
  while True:
    
    user_choice = input("\nТвой ход. Напиши камень, ножницы или бумага. Для выхода напиши 0.").lower()
    
    # Проверка на выход
    if user_choice == "0":
      print("Спасибо за игру, до свидания!")
      break
    
    # Проверка ввода
    if user_choice not in options:
      print("Ошибка! Напиши именно 'камень', или 'ножницы', или 'бумага'.")
      continue
    
    # Компьютер выбирает
    computer_choice = random.choice(options)
    print(f"Компьютер выбрал: {computer_choice}")
    
    # Выявляем победителя
    # Если ничья
    if user_choice == computer_choice:
      print("Ничья! Играем еще раз.")
    
    # Если победил пользователь
    elif ((user_choice=="камень" and computer_choice == "ножницы") or (user_choice=="ножницы" and computer_choice == "бумага") or (user_choice=="бумага" and computer_choice == "камень")):
      print("Ты победил!")
    
    else:
      print("Победил компьютер!")
  
  # Запуск игры
if __name__ == "__main__":
  game()

