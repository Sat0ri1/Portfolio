#_________________________ METODA 1 - MC _______________________________

set.seed(123)

# Funkcja sprawdzająca czy punkt lezy wewnatrz okręgu(jeśli odległość of środka kwadratu
# byłaby dłuższa od promienia okręgu, to punkt jest na zewnątrz)
p_in_circle <- function(x, y) {
  return(x^2 + y^2 <= 1)
}

#------------------------------------------------------------------

# Funkcja przyblizajaca π za pomocą metody 1
monte_carlo_pi1 <- function(num_points) {
  in_circle <- 0
  points_in_circle <- matrix(0, ncol = 2, nrow = num_points)
  points_outside_circle <- matrix(0, ncol = 2, nrow = num_points)
  
  for (i in 1:num_points) {
    x <- runif(1, min = -1, max = 1)
    y <- runif(1, min = -1, max = 1)
    
    if (p_in_circle(x, y)) {
      in_circle <- in_circle + 1
      points_in_circle[in_circle, ] <- c(x, y)
    } else {
      points_outside_circle[i - in_circle, ] <- c(x, y)
    }
  }
  

  points_outside_circle <- points_outside_circle[complete.cases(points_outside_circle), ]
  
  # Wykres dla Metody 1
  plot_monte_carlo(points_in_circle, points_outside_circle, "Metoda 1 (kwadrat w okręgu)", num_points)
  
  return(4 * in_circle / num_points)
}

#__________________________ METODA 2 - MC __________________________________

# Funkcja przyblizajaca π za pomoca Metody 2
monte_carlo_pi2 <- function(num_points) {
  in_sphere <- 0
  points_in_sphere <- matrix(0, ncol = 3, nrow = num_points)
  points_outside_sphere <- matrix(0, ncol = 3, nrow = num_points)
  
  for (i in 1:num_points) {
    
    # Generowanie losowych punktow wewnatrz szescienu
    x <- runif(1, min = -1, max = 1)
    y <- runif(1, min = -1, max = 1)
    z <- runif(1, min = -1, max = 1)
    
    # Sprawdzanie, czy punkt lezy wewnatrz kuli(jeśli odległość of środka sześcianu
    # byłaby dłuższa od promienia kuli, to punkt jest na zewnątrz)
    distance <- sqrt(x^2 + y^2 + z^2)
    
    if (distance <= 1) {
      in_sphere <- in_sphere + 1
      points_in_sphere[in_sphere, ] <- c(x, y, z)
    } else {
      points_outside_sphere[i - in_sphere, ] <- c(x, y, z)
    }
  }
  
  points_outside_sphere <- points_outside_sphere[complete.cases(points_outside_sphere), ]
  
  # Wykres dla Metody 2
  plot_monte_carlo(points_in_sphere, points_outside_sphere, "Metoda 2 (kula w szescianie)", num_points)
  
  # Estymacja liczby π na podstawie stosunku objetosci kuli do objetosci szescianu
  return(6 * in_sphere / num_points)
}

#___________________________ WYKRESY - MC ___________________________________

# Funkcja rysująca wykres dla metody Monte Carlo
plot_monte_carlo <- function(points_in, points_outside, title, num_points) {
  par(mfrow=c(1,2))  # Set up a 1x2 plotting grid for side-by-side plots
  
  # Pkt wewnatrz
  plot(points_in[, 1], points_in[, 2], col = "blue", pch = 16, main = title, 
       xlab = "Oś X", ylab = "Oś Y", xlim = c(-1, 1), ylim = c(-1, 1))
  
  # Pkt na zewnatrz
  points(points_outside[, 1], points_outside[, 2], col = "red", pch = 16)
  
  # Punkt w srodku
  if (any(points_outside == 0)) {
    points(0, 0, col = "green", pch = 16)
  }
  
  legend("topright", legend = c("Wewnątrz", "Na zewnątrz", "Środek"), col = c("blue", "red", "green"), pch = 16)
  
  
  par(mfrow=c(1,1))
}



#__________________________ CZAS - MC _________________________________

# Funkcja mierząca czas wykonania metody Monte Carlo
measure_time <- function(method_function, num_points) {
  start_time <- Sys.time()
  result <- method_function(num_points)
  end_time <- Sys.time()
  elapsed_time <- end_time - start_time
  
  return(list(
    result = result,
    elapsed_time = elapsed_time
  ))
}


#________________________ WYBORY - MC ________________________________

# Funkcja do wyboru metody
choose_method <- function() {
  cat("Wybierz metodę:\n")
  cat("1. Metoda 1 (kwadrat w okręgu)\n")
  cat("2. Metoda 2 (kula w szescianie)\n")
  cat("3. Obie metody\n")
  
  choice <- as.numeric(readline("Twój wybór: "))
  
  if (choice %in% c(1, 2, 3)) {
    return(choice)
  } else {
    cat("Nieprawidłowy wybór. Spróbuj ponownie.\n")
    choose_method()
  }
}


#____________________________ USER LOOP - MC _________________________________

# Funkcja z petla wywolujaca do pi monte carlo
pi_loop <- function() {
  repeat {
    selected_method <- choose_method()
    
    # Metoda 1
    if (selected_method == 1 || selected_method == 3) {
      num_points <- as.numeric(readline("Podaj liczbę punktów dla Metody 1: "))
      result_1 <- measure_time(monte_carlo_pi1, num_points)
      approx_pi1 <- result_1$result
      
      cat("Metoda 1 (okrąg w kwadracie) - Przybliżone π:", approx_pi1, "\nRzeczywiste π:", pi, "\nBłąd:", abs(approx_pi1 - pi), "\n",
          "Czas wykonania:", result_1$elapsed_time, "sekundy\n\n")
    }
    
    # Metoda 2
    if (selected_method == 2 || selected_method == 3) {
      num_points <- as.numeric(readline("Podaj liczbę punktów dla Metody 2: "))
      result_2 <- measure_time(monte_carlo_pi2, num_points)
      approx_pi2 <- result_2$result
      
      cat("Metoda 2 (kula w szescianie) - Przybliżone π:", approx_pi2, "\nRzeczywiste π:", pi, "\nBłąd:", abs(approx_pi2 - pi), "\n",
          "Czas wykonania:", result_2$elapsed_time, "sekundy\n\n")
    }
    
    # Powtorka
    repeat_choice <- tolower(readline("Czy chcesz kontynuować przyblizanie pi? (tak/nie): "))
    if (repeat_choice %in% c("tak", "nie")) {
      if (repeat_choice == "nie") {
        break
      }
    } else {
      cat("Błędna odpowiedź. Zamykanie programu.\n")
      break
    }
  }
}

#__________________________ RNORM - ROZKLAD NORMALNY_________________________________
# Generator korzystający z funkcji rnorm()

generator_1 <- function(n, mean, sd){
  rnorm(n,mean,sd)
}

#_________________________ BOX MULLER - RN______________________________

# Generator korzystający z metody boxa mullera

box_muller <- function(n, mean, sd) {
  
  # Sprawdzenie, czy liczba n jest parzysta
  if (n %% 2 != 0) {
    stop("Liczba n musi być liczbą parzystą")
  }
  
  # Inicjalizacja wektorów o wartościach 0 na liczby losowe
  z1 <- numeric(n/2)
  z2 <- numeric(n/2)
  
  # Generowanie liczb losowych z rozkładu normalnego
  for (i in 1:(n/2)) {
    u1 <- runif(1)
    u2 <- runif(1)
    
    # Stosujemy wzory na Z1 i Z2
    v1 <- sqrt(-2 * log(u1)) * cos(2 * pi * u2)
    v2 <- sqrt(-2 * log(u1)) * sin(2 * pi * u2)
    
    z1[i] <- v1
    z2[i] <- v2
  }
  
  # przemnażamy otrzymane wartości razy założone odchylenie std i dodajemy wartość założonej średniej
  result <- c(z1, z2) * sd + mean
  
  return(result)
}

#_______________________ METODA ODWROTNEJ DYSTRYBUANTY - RN ___________________________  


Metoda_odw <- function(n, mean, sd){
  
  #  funkcja generująca n losowych zmiennych z rozkładu jednostajnego(0, 1)
  u <- runif(n)
  
  # używamy odwrotnej dystrybuanty roz norm do przekształcenia zmiennych jednostajnych
  random_numbers <- qnorm(u)
  
  # przemnażamy otrzymaną wartość razy założone odchylenie std i dodajemy wartość założonej średniej
  wynik <- random_numbers * sd + mean
  return(wynik)
}

#______________________________ MARS - RN ___________________________________________

mars <- function(n, mean, sd) {
  result <- numeric(n)
  
  for (i in seq_along(result)) {
    while (TRUE) {
      V1 <- 2 * runif(1) - 1
      V2 <- 2 * runif(1) - 1
      
      S <- V1^2 + V2^2
      
      if (S < 1) {
        X <- sqrt(-2 * log(S) / S)
        result[i] <- mean + sd * V1 * X
        break
      }
    }
  }
  
  return(result)
}


#_______________________ WYBORY RN ___________________________________

normal_loop <- function() {
  repeat {
    cat("Wybierz metodę generacji próbek:\n")
    cat("1. rnorm\n")
    cat("2. Box-Mullera\n")
    cat("3. Metoda Odwrotnej Dystrybuanty\n")
    cat("4. Marsaglia Polar\n")
    cat("5. Wszystkie metody\n")
    
    method <- as.character(readline("Wprowadź numer metody: "))
    
    if (!method %in% c("1", "2", "3", "4", "5")) {
      cat("Błędny numer metody. Spróbuj ponownie.\n")
      next
    }
    
    # Wprowadzanie parametrow
    n <- as.numeric(readline("Wprowadź rozmiar próby: "))
    mean_val <- as.numeric(readline("Wprowadź średnią: "))
    sd_val <- as.numeric(readline("Wprowadź odchylenie standardowe: "))
    
    elapsed_times <- NULL
    
    # Wybor metody
    if (method == "1") {
      start_time <- Sys.time()
      samples <- generator_1(n, mean_val, sd_val)
      end_time <- Sys.time()
      elapsed_time <- end_time - start_time
      elapsed_times <- c(elapsed_times, generator_1 = elapsed_time)
    } else if (method == "2") {
      start_time <- Sys.time()
      samples <- box_muller(n, mean_val, sd_val)
      end_time <- Sys.time()
      elapsed_time <- end_time - start_time
      elapsed_times <- c(elapsed_times, box_muller = elapsed_time)
    } else if (method == "3") {
      start_time <- Sys.time()
      samples <- Metoda_odw(n, mean_val, sd_val)
      end_time <- Sys.time()
      elapsed_time <- end_time - start_time
      elapsed_times <- c(elapsed_times, Metoda_odw = elapsed_time)
    } else if (method == "4") {
      start_time <- Sys.time()
      samples <- mars(n, mean_val, sd_val)
      end_time <- Sys.time()
      elapsed_time <- end_time - start_time
      elapsed_times <- c(elapsed_times, mars = elapsed_time)
    } else if (method == "5") {
      start_time_rnorm <- Sys.time()
      samples_rnorm <- generator_1(n, mean_val, sd_val)
      end_time_rnorm <- Sys.time()
      elapsed_time_rnorm <- end_time_rnorm - start_time_rnorm
      elapsed_times <- c(elapsed_times, rnorm = elapsed_time_rnorm)
      
      start_time_box_muller <- Sys.time()
      samples_box_muller <- box_muller(n, mean_val, sd_val)
      end_time_box_muller <- Sys.time()
      elapsed_time_box_muller <- end_time_box_muller - start_time_box_muller
      elapsed_times <- c(elapsed_times, box_muller = elapsed_time_box_muller)
      
      start_time_inverse_transform <- Sys.time()
      samples_inverse_transform <- Metoda_odw(n, mean_val, sd_val)
      end_time_inverse_transform <- Sys.time()
      elapsed_time_inverse_transform <- end_time_inverse_transform - start_time_inverse_transform
      elapsed_times <- c(elapsed_times, inverse_transform = elapsed_time_inverse_transform)
      
      start_time_marsaglia_polar <- Sys.time()
      samples_marsaglia_polar <- mars(n, mean_val, sd_val)
      end_time_marsaglia_polar <- Sys.time()
      elapsed_time_marsaglia_polar <- end_time_marsaglia_polar - start_time_marsaglia_polar
      elapsed_times <- c(elapsed_times, marsaglia_polar = elapsed_time_marsaglia_polar)
      
      samples <- list(
        rnorm = samples_rnorm,
        box_muller = samples_box_muller,
        inverse_transform = samples_inverse_transform,
        marsaglia_polar = samples_marsaglia_polar
      )
    }
    
    
    # Wyswietlanie prob
    if (is.list(samples)) {
      cat("\nWartości prób dla metody wszystkich metod", ":\n")
      for (method_name in names(samples)) {
        cat(paste(method_name, ":\n"))
        print(samples[[method_name]])
        cat("\n")
      }
    } else {
      cat("\n Wartosci proby dla wybranej metody:\n")
      print(samples)
    }
    
    
    # Wyswietlanie czasu dzialania
    if (is.list(samples)) {
      for (method_name in names(samples)) {
        cat("Czas generacji próbki (", method_name, "):", elapsed_times[method_name], "sekundy\n")
      }
    } else {
      cat("Czas generacji próbki:", elapsed_times, "sekundy\n")
    }
    
    cat("\n")
    
    # Histogramy
    if (is.list(samples)) {
      par(mfrow = c(2, 2))
      for (method_name in names(samples)) {
        hist(samples[[method_name]], main = paste("Histogram -", method_name),
             xlab = "Wartości", col = "lightblue")
      }
      par(mfrow = c(1, 1))
    } else {
      hist(samples, main = "Histogram", xlab = "Wartości", col = "lightblue")
    }
    
    # Test shapiro wilka
    if (is.list(samples)) {
      cat("Testy Shapiro-Wilka:\n")
      for (method_name in names(samples)) {
        shapiro_test_result <- shapiro.test(samples[[method_name]])
        cat(paste(method_name, "Wartość p:", shapiro_test_result$p.value), "\n")
      }
    } else {
      shapiro_test_result <- shapiro.test(samples)
      cat("Test Shapiro-Wilka:\n")
      cat(paste("Wartość p:", shapiro_test_result$p.value), "\n")
    }
    
    # Zapisywanie do pliku
    save_samples <- tolower(readline("Czy chcesz zapisać próby do pliku? (tak/nie): "))
    if (save_samples == "tak") {
      file_name <- readline("Podaj nazwę pliku (bez rozszerzenia): ")
      extension <- tolower(readline("Wybierz rozszerzenie pliku (txt/rds): "))
      
      if (is.list(samples)) {
        for (method_name in names(samples)) {
          if (extension == "txt") {
            write.table(samples[[method_name]], file = paste0(file_name, "_", method_name, ".txt"), row.names = FALSE, col.names = FALSE)
          } else if (extension == "rds") {
            saveRDS(samples[[method_name]], file = paste0(file_name, "_", method_name, ".rds"))
          }
        }
        cat("Wszystkie próby zostały zapisane do plikow: ", paste0(file_name, "_<metoda>.", extension), "\n")
      } else {
        if (extension == "txt") {
          write.table(samples, file = paste0(file_name, ".txt"), row.names = FALSE, col.names = FALSE)
        } else if (extension == "rds") {
          saveRDS(samples, file = paste0(file_name, ".rds"))
        }
        cat("Próba została zapisana do pliku: ", paste0(file_name, ".", extension), "\n")
      }
    }
    
    # Powtorzenie
    repeat_choice <- tolower(readline("Czy chcesz wygenerować kolejne próby? (tak/nie): "))
    
    # sprawdzanie inputu
    if (repeat_choice %in% c("tak", "nie")) {
      if (repeat_choice == "nie") {
        break
      }
    } else {
      cat("Błędna odpowiedź. Zamykanie programu.\n")
      break
    }
  }
}



# Wybor dzialania
choose_use <- function() {
  cat("Co chcesz zrobić:\n")
  cat("1. Generowanie liczb losowych dla rozkladu normalnego\n")
  cat("2. Generowanie zmiennych z rozkladu Wisharta\n")
  cat("3. Przyblizanie liczby π przy pomocy metod Monte Carlo\n")
  cat("4. To juz wszystko, chce wylaczyc program\n")
  
  choice <- as.numeric(readline("Twój wybór: "))
  
  if (choice %in% c(1, 2, 3, 4)) {
    return(choice)
  } else {
    cat("Nieprawidłowy wybór. Spróbuj ponownie.\n")
    choose_use()
  }
}

#______________________ FUNKCJA - WISHART ___________________________
set.seed(123)

wishart <- function(n, df, Sigma) {
  d <- ncol(Sigma)
  
  # Pusta lista na proby
  samples <- list()
  
  for (i in 1:n) {
    
    # generowanie macierzy ze standardowego rozkładu normalnego
    Z <- matrix(rnorm(d * df), nrow = df)
    
    # Macierz kowariancji za pomocą faktoryzacji macierzy Z
    C <- chol(Sigma)
    
    # Przeskalowywanie macierzy kowariancji przez macierz skali Sigma
    X <- Z %*% C
    
    # Obliczanie  iloczynu t(X) (transonowanej macierzy X) i oryginalnej macierzy X 
    M <- t(X) %*% X
    
    # Dodawanie proby do listy
    samples[[i]] <- M
  }
  
  return(samples)
}
#________________________ USER LOOP - WISHART ________________________
wishart_loop <- function() {
  repeat {
    
    # Pobieranie n i df
    n <- as.numeric(readline("Wprowadź liczbę prób (n): "))
    df <- as.numeric(readline("Wprowadź stopnie swobody (df): "))
    
    # Sprawdzanie czy wprowadzono prawidlowe n i df
    if (!is.numeric(n) || !is.numeric(df) || n <= 0 || df <= 0) {
      cat("Błędne dane. Spróbuj ponownie.\n")
      next
    }
    
    # Definicja macierzy
    Sigma <- matrix(c(2, 0.5, 0.5, 0.5, 2, 0.5, 0.5, 0.5, 2), nrow = 3)
    
    # Generowanie
    set.seed(123)
    Wishart_samples <- wishart(n, df, Sigma)
    
    # Wyswietlanie wynikow
    cat("Wyniki dla n =", n, "i df =", df, ":\n")
    print(Wishart_samples)
    
    compare_choice <- tolower(readline("Czy chciałbyś porównać wynik z próbą otrzymaną funkcją rWishart? (tak/nie): "))
    if (compare_choice == "tak"){
      set.seed(123)
      cat("Wyniki rWishart dla n =", n, "i df =", df, ":\n")
      to_compare <- rWishart(n, df, Sigma)
      print(to_compare)
    }
    
    # Zapisywanie do pliku
    save_samples <- tolower(readline("Czy chcesz zapisać próby do pliku? (tak/nie): "))
    if (save_samples == "tak") {
      file_name <- readline("Podaj nazwę pliku (bez rozszerzenia): ")
      extension <- tolower(readline("Wybierz rozszerzenie pliku (txt/rds): "))
      
      if (extension == "txt") {
        write.table(Wishart_samples, file = paste0(file_name, ".txt"), row.names = FALSE, col.names = FALSE)
      } else if (extension == "rds") {
        saveRDS(Wishart_samples, file = paste0(file_name, ".rds"))
      }
      cat("Próby zostały zapisane do pliku: ", paste0(file_name, ".", extension), "\n")
    }
    
    
    # Powtorzenie
    repeat_choice <- tolower(readline("Czy chcesz kontynuować? (tak/nie): "))
    if (repeat_choice %in% c("tak", "nie")) {
      if (repeat_choice == "nie") {
        break
      }
    } else {
      cat("Błędna odpowiedź. Zamykanie programu.\n")
      break
    }
  }
}

#________________________ PETLA GLOWNA _________________________________

repeat {
  selected_use <- choose_use()
  if (selected_use == 1) {normal_loop()}
  if (selected_use == 2) {wishart_loop()}
  if (selected_use == 3) {pi_loop()}
  if (selected_use == 4) {
    cat("Do zobaczenia!\n")
    break
  }
}

