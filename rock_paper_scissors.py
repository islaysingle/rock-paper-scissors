import random
import os
import json
from phrases import phrases, intro_messages, outro_messages
from avatars import AVATARS


# Функция информации о персонажах
def print_info_about_avatars():
  print(f"=== Вот кто эти люди: ===")
  print(f"Василий: {AVATARS['vasily']['bio']}")
  print(f"Василиxса: {AVATARS['vasilisa']['bio']}")
  print("================================================")

# Функция выбора персонажа
def show_avatar_selection():
  print(f"\n--- Выбери персонажа ---")
  
  # Рисуем меню
  print(f"1. Василий")
  print(f"2. Василиса")
  print(f"12345. Кто эти люди?")
  print(f"0. Выход")
  
  while True:
    choice = input("Твой выбор: ")
    
    # Обрабатываем выбор
    if choice == "1":
      return "vasily"
    elif choice == "2":
      return "vasilisa"
    elif choice == "12345":
      print_info_about_avatars()
    elif choice == 0:
      return None
    else:
      print(f"Нет такого варианта. Выбери варианты, которые есть в меню.")

# Функция проверки, сохранения, загрузки профиля игрока
def get_user_profile():
  file_name = "user_profile.json"
  
  # 1. Проверяем, есть ли файл. 
  # Если файл есть и игрок хочет продолжить играть за последнего персонажа - загружаем сохраненный профиль.
  if os.path.exists(file_name):
    with open(file_name, "r", encoding="utf-8") as f:
      profile = json.load(f)
    
    avatar_id = profile["avatar_id"]
    avatar_name = AVATARS[avatar_id]["name"]
    
    print(f"\nПривет! Меня зовут Виктория. {avatar_name}, это ты?")
    print(f"\nНапиши да, чтобы продолжить играть за {avatar_name}.")
    print(f"\nНапиши нет, чтобы выбрать персонажа.")
    
    answer = input(">").lower()
    
    if answer == "да":
      return profile # Возвращаем профиль из сохранения
    else:
      print("ОК, тогда выбери себе персонажа.")
  # 2. Если игрок хочет начать заново, предлагаем выбрать персонажа.
  selected_avatar_id = show_avatar_selection()
  
  # Проверка на выход из игры
  if selected_avatar_id is None:
    return None
  
  # Создаем новый профиль
  new_profile = {
    "avatar_id": selected_avatar_id,
    "stats": {
      "wins": 0,
      "losses": 0,
      "draws": 0
    }
  }
  return new_profile

# Функция сохранения профиля в файл
def save_profile(profile):
  file_name = "user_profile.json"
  with open(file_name, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False)
  
# Основная функция игры. Принимает профиль - словарь с ID аватара и статистикой с прошлых игр.
def game(profile):
  
  # Список вариантов
  options = ["камень", "ножницы", "бумага"]
  
  # 1. Подготовка данных
  avatar_id = profile["avatar_id"]
  avatar_name = AVATARS[avatar_id]["name"]
  
  # Достаем статистику из файла профиля
  stats = profile.get("stats", {"wins":0, "losses":0, "draws":0})
  user_wins = stats["wins"]
  computer_wins = stats["losses"]
  match_draws = stats["draws"]
  
  # Случайное приветствие
  print("\n"+"="*30)
  print(random.choice(intro_messages[avatar_id]))
  print("="*30)
  
  # Главный цикл игры
  while True:
    
    user_choice = input(f"\nТвой ход, {avatar_name}. Напиши камень, ножницы или бумага. Для выхода напиши q. ").lower()
    
    # Проверка на выход
    if user_choice == "q":
      print("===========================================")
      print(f"ИГРА ОКОНЧЕНА!")
      print(f"Побед: {user_wins}.")
      print(f"Поражений: {computer_wins}.")
      
      if user_wins > computer_wins:
        print(f"Победа в общем зачете! Поздравляю!")
      elif computer_wins > user_wins:
        print(f"Поражение в общем зачете. Возможно, в следующий раз повезет больше!")
      else:
        print(f"В общем зачете ничья!")
      print("===========================================")
      print("\n"+random.choice(outro_messages[avatar_id]))
      print("===========================================")
      break
    
    # Проверка ввода
    if user_choice not in options:
      print("Ошибка! Напиши именно 'камень', или 'ножницы', или 'бумага'.")
      continue
    
    # Компьютер выбирает
    computer_choice = random.choice(options)
    print(f"Я выбираю: {computer_choice}")
    
    # Выявляем результат и определяем фразу.
    result_key=""
    
    # Если ничья
    if user_choice == computer_choice:
      print("Ничья! Играем еще раз.")
      match_draws+=1
      result_key = "draw"
    
    # Если победил пользователь
    elif ((user_choice=="камень" and computer_choice == "ножницы") or (user_choice=="ножницы" and computer_choice == "бумага") or (user_choice=="бумага" and computer_choice == "камень")):
      print("Победа за тобой!")
      user_wins +=1
      result_key="win"
    
    else:
      print("Я победила!")
      computer_wins +=1
      result_key="lose"
    
    # Подбираем фразу для аватара и результата
    final_phrases = list(phrases["common"][result_key])
    avatar_phrases = phrases.get(avatar_id, {}).get(result_key, [])
    final_phrases+=avatar_phrases
    
    if final_phrases:
      print(random.choice(final_phrases))
    
    # Выводим счет после каждого раунда.
    print(f"Текущий счет:    Ты: {user_wins}    Компьютер: {computer_wins}")
    
  # Сохранение статистики
  profile["stats"]={
    "wins": user_wins,
    "losses": computer_wins,
    "draws": match_draws
  }
  
# Запуск игры

if __name__ == "__main__":
  print("Hello world!")
  
  print("==============================")
  print("==  Камень Ножницы Бумага  ==")
  print("==============================")
  # Получаем профиль или создаем нвоый:
  current_profile = get_user_profile()
  
  # Если профиль получен, то играем
  if current_profile:
    game(current_profile)
    save_profile(current_profile)
  # Если профиля нет, то уходим.
  else:
    print("До свидания! Заходи как-нибудь...")

