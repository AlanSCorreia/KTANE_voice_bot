import speech_recognition as sr
import pygame


def audio(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def recognizer(rec):
    with sr.Microphone() as mic:
        rec.adjust_for_ambient_noise(mic, duration=0.5)
        audio = rec.listen(mic)
        frase = rec.recognize_google(audio, language="pt-BR")
        return frase.split(' ')


# Variaveis
pygame.init()
frases_quita = ["fim de operação", "operação bem sucedida"]
fios_simples = {

}
voz = sr.Recognizer()


class Bomba:
    def __init__(self, qntd_pilhas, serial, entrada_paralela, entrada_ethernet, indicador_car, indicador_frk):
        self.qntd_pilhas = qntd_pilhas
        self.serial = serial
        self.entrada_paralela = entrada_paralela
        self.entrada_ethernet = entrada_ethernet
        self.indicador_car = indicador_car
        self.indicador_frk = indicador_frk


class FiosSimples:
    def __init__(self, qntd, lista_fios):
        self.qntd = qntd
        if len(lista_fios) == self.qntd:
            self.lista_fios = lista_fios

    def resolver(self, bomba):
        match self.qntd:

            case 3:
                if "vermelho" not in self.lista_fios:
                    print("Corte o segundo fio.")
                elif self.lista_fios[-1] == "branco":
                    print("Corte o último fio.")
                elif self.lista_fios.count("azul") > 1:
                    print("Corte o último fio azul.")
                else:
                    print("Corte o último fio.")

            case 4:
                if self.lista_fios.count("vermelho") > 1 and int(bomba.serial[-1]) % 2 == 1:
                    print("Corte o último fio vermelho.")
                elif self.lista_fios.count("vermelho") == 0 and self.lista_fios[-1] == "amarelo":
                    print("Corte o primeiro fio.")
                elif self.lista_fios.count("azul") == 1:
                    print("Corte o primeiro fio.")
                elif self.lista_fios.count("amarelo") > 1:
                    print("Corte o último fio.")
                else:
                    print("Corte o segundo fio.")

            case 5:
                if self.lista_fios[-1] == "preto" and int(bomba.serial[-1]) % 2 == 1:
                    print("Corte o quarto fio.")
                elif self.lista_fios.count("vermelho") == 1 and self.lista_fios.count("amarelo") > 1:
                    print("Corte o primeiro fio.")
                elif self.lista_fios.count("preto") == 0:
                    print("Corte o segundo fio.")
                else:
                    print("Corte o primeiro fio.")

            case 6:
                if self.lista_fios.count("amarelo") == 0 and int(bomba.serial[-1]) % 2 == 1:
                    print("Corte o terceiro fio.")
                elif self.lista_fios.count("amarelo") == 1 and self.lista_fios.count("branco") > 1:
                    print("Corte o quarto fio.")
                elif self.lista_fios.count("vermelho") == 0:
                    print("Corte o último fio.")
                else:
                    print("Corte o quarto fio.")


class Botao:
    def __init__(self, cor, escrito):
        self.cor = cor
        self.escrito = escrito
        self.luz = {
            "azul": audio("audio/KNTE - 4_any_pos.mp3"),
            "branca": audio("audio/KNTE - 1_any_pos.mp3"),
            "amarela": audio("audio/KNTE - 5_any_pos.mp3"),
            "outra": audio("audio/KNTE - 1_any_pos.mp3")
        }

    def set_cor(self):

        audio("audio/KNTE - pressione e espere.mp3")
        audio("audio/KNTE - qual faixa.mp3")
        luz = input()

        if luz in self.luz:
            print(f"{self.luz[luz]}")
        else:
            print(f"{self.luz['outra']}")

    def resolver(self, b):

        if b.qntd_pilhas > 1 and self.escrito == "detonar":
            audio("audio/KNTE - pressione e solte o botao.mp3")
        elif self.escrito == "segurar" and self.cor == "vermelho":
            audio("audio/KNTE - pressione e solte o botao.mp3")
        elif b.qntd_pilhas > 2 and b.indicador_frk:
            audio("audio/KNTE - pressione e solte o botao.mp3")

        match self.cor:

            case "azul":
                if self.escrito == "abortar":
                    self.set_cor()
                else:
                    audio("audio/KNTE - pressione e espere.mp3")

            case "branco":
                if b.indicador_car:
                    self.set_cor()
                else:
                    audio("audio/KNTE - pressione e espere.mp3")

            case "amarelo":
                self.set_cor()

            case "vermelho":
                if self.escrito == "segure":
                    audio("audio/KNTE - pressione e solte o botao.mp3")
                else:
                    audio("audio/KNTE - pressione e espere.mp3")


if __name__ == "__main__":
    bomba = Bomba(4, "ABC!@#5", True, True, False, False)

    while True:

        pergunta = recognizer(voz)
        if pergunta[0] == "resolver":
            match pergunta[1]:
                case "botao":
                    cor = recognizer(voz)
                    Botao(
                        input("Informe a cor do botao: "),
                        input("Informe a frase escrita no botao")
                    ).resolver(bomba)

                case "fios":
                    if pergunta[2] == "simples":
                        audio("audio/KNTE - quantos fios tem o modulo.mp3")
                        qntd = 0

                        while qntd not in range(3, 7):
                            try:
                                qntd = int(recognizer(voz)[0])
                            except ValueError:
                                continue

                        audio("audio/KNTE - cores dos fios.mp3")
                        cores = recognizer(sr.Recognizer).split(' ')
                        FiosSimples(
                            qntd,
                            cores
                        ).resolver(bomba)

        elif pergunta[0] == "sair" or pergunta[0] == "fechar":
            break
