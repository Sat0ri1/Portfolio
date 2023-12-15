sciezka <- readline(prompt = "Podaj ścieżkę do pliku: ")
dane <- read.csv2(sciezka)
ans <- readline(prompt = "jesli chcesz przeprowadzic test dla 2 prob, wpisz 'tak', jeśli dla jednej, wpisz 'nie': ")


head(dane)
if (ans =="nie") {
  column <- readline(prompt = "podaj kolumę dla próby: ")
  column <- as.numeric(column)
  dane <- dane[,column]
  mu0 <- readline(prompt = "Podaj średnią z populacji dla próby: ")
  mu0 <- as.numeric(mu0)
  alternatywa <- readline(prompt = "Wybierz hipotezę alternatywną: '0' srednia z proby jest rozna od sredniej z populacji, '1' srednia z proby jest wieksza od sredniej z populacji, '2' srednia z proby jest mniejsza od sredniej z populacji:  ")
 
  t_test = function(dane, mu0, alternatywa) {
    mean_x = mean(dane)
    sd_x = sd(dane)
    n_x = length(dane)
    df_x = n_x - 1
    t = sqrt(n_x)*(mean_x-mu0)/sd_x
    if (alternatywa == 0) {
      p_value = pt(t, df_x)
    } else if (alternatywa == 1) {
      p_value = pt(t, df_x, lower.tail = FALSE)        
    } else {
      p_value = 2*pt(abs(t), df_x, lower.tail = FALSE)
    }
    list(statystyka = t, p = p_value)
  }
  t_test(dane, mu0, alternatywa)
}

if (ans == "tak") {
  col1 <- readline(prompt = "podaj kolumę dla 1 próby: ")
                   col2 <- readline(prompt = "podaj kolumnę dla 2 próby: ")
                        col1 <- as.numeric(col1)
                        col2 <- as.numeric(col2)
                                    dane1 <- dane[,col1]
                                    dane2 <- dane[,col2]
}

if (ans == "tak") {
  ans2<-readline(prompt = "Jeśli chcesz wykonać test t dla prób zależnych wpisz 'tak', jeśli dla niezależnych, wpisz 'nie': ")
  alternatywa <- readline(prompt = "Wybierz hipotezę alternatywną: '0' srednie z prób są różne, '1' srednia z proby pierwszej jest większa, '2' srednia z proby pierwszej jest mniejsza:  ")
}

if (ans == "tak" & ans2 == "nie"){
  nasz_t_test2 = function(dane1, dane2, alternatywa) {    
    mean_x = mean(dane1)
    var_x = var(dane1)
    n_x = length(dane1)
    mean_y = mean(dane2)
    var_y = var(dane2)
    n_y = length(dane2)
    df = n_x + n_y - 2
    t = (mean_x-mean_y)/sqrt((n_x-1)*var_x+(n_y-1)*var_y)*sqrt((n_x*n_y*df) / (n_x+n_y))
    if (alternatywa == 0) {
      p_wartosc = pt(t, df)
    } else if (alternatywa == 1) {
      p_wartosc = pt(t, df, lower.tail = FALSE)        
    } else {
      p_wartosc = 2*pt(abs(t), df, lower.tail = FALSE)
    }
    list(statystyka = t, p = p_wartosc)
  }
  nasz_t_test2(dane1, dane2, alternatywa)
}

if (ans == "tak" & ans2 =="tak") {
  nasz_t_test3 = function(dane1, dane2, alternatywa) {
    d = dane1 - dane2
    mean_d = mean(d)
    sd_d = sd(d)
    n_d = length(d)
    df_d = n_d - 1
    t = sqrt(n_d)*mean_d/sd_d
    if (alternatywa == 0) {
      p_wartosc = pt(t, df_d)
    } else if (alternatywa == 1) {
      p_wartosc = pt(t, df_d, lower.tail = FALSE)        
    } else {
      p_wartosc = 2*pt(abs(t), df_d, lower.tail = FALSE)
    }
    list(statystyka = t, p = p_wartosc)
  }
  nasz_t_test3(dane1, dane2, alternatywa)
}
