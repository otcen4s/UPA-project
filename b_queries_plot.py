import pandas as pd
pd.options.plotting.backend = "plotly"
from plotly.subplots import make_subplots
import plotly.graph_objects as go



def plot_graph_task1(name, output_fig, quartal_time):
    

    col_list = ["datum", "prirastok", "kraj", "pocet_nakazenych_per_capita", "celkovy_pocet_obyvatelov", "celkovy_pocet_nakazenych"]
    data = pd.read_csv(name, usecols=col_list)


    kraj_praha = data.loc[data['kraj'] == 'Praha']
    kraj_stredocesky = data.loc[data['kraj'] == 'Stredocesky']
    kraj_jihocesky = data.loc[data['kraj'] == 'Jihocesky']
    kraj_plzneksy = data.loc[data['kraj'] == 'Plzensky']
    kraj_karlovarsky = data.loc[data['kraj'] == 'Karlovarsky']
    kraj_ustecky = data.loc[data['kraj'] == 'Ustecky']
    kraj_liberecky = data.loc[data['kraj'] == 'Liberecky']
    kraj_kralovehradecky = data.loc[data['kraj'] == 'Kralovehradecky']
    kraj_pardubicky = data.loc[data['kraj'] == 'Pardubicky']
    kraj_vysocina = data.loc[data['kraj'] == 'Vysocina']
    kraj_jihomoravsky = data.loc[data['kraj'] == 'Jihomoravsky']
    kraj_olomoucky = data.loc[data['kraj'] == 'Olomoucky']
    kraj_zlinsky = data.loc[data['kraj'] == 'Zlinsky']
    kraj_moravskoslezsky = data.loc[data['kraj'] == 'Moravskoslezsky']
    
    
    fig = make_subplots(rows=7, cols=2, subplot_titles=("Praha", "Stredočeský", "Jihočeský", "Plzenský", "Karlovarský", 
    "Ústecký", "Liberecký", "Kralovehradecký", "Pardubický", "Vysočina", "Jihomoravský", "Olomoucký", "Zlínsky", "Moravskoslezský"))

    # Graphs for day incidence 
    fig.add_trace(go.Scatter(x=kraj_praha["datum"], y=kraj_praha["prirastok"], name="Praha"),row=1, col=1)
    fig.add_trace(go.Scatter(x=kraj_stredocesky["datum"], y=kraj_stredocesky["prirastok"], name="Stredočeký"),row=1, col=2)
    fig.add_trace(go.Scatter(x=kraj_jihocesky["datum"], y=kraj_jihocesky["prirastok"], name="Jihočeský"),row=2, col=1)
    fig.add_trace(go.Scatter(x=kraj_plzneksy["datum"], y=kraj_plzneksy["prirastok"], name="Plzenský"),row=2, col=2)
    fig.add_trace(go.Scatter(x=kraj_karlovarsky["datum"], y=kraj_karlovarsky["prirastok"], name="Karlovarský"),row=3, col=1)
    fig.add_trace(go.Scatter(x=kraj_ustecky["datum"], y=kraj_ustecky["prirastok"], name="Ústecký"),row=3, col=2)
    fig.add_trace(go.Scatter(x=kraj_liberecky["datum"], y=kraj_liberecky["prirastok"], name="Liberecký"),row=4, col=1)
    fig.add_trace(go.Scatter(x=kraj_kralovehradecky["datum"], y=kraj_kralovehradecky["prirastok"], name="Kralovehradecký"),row=4, col=2)
    fig.add_trace(go.Scatter(x=kraj_pardubicky["datum"], y=kraj_pardubicky["prirastok"], name="Pardubický"),row=5, col=1)
    fig.add_trace(go.Scatter(x=kraj_vysocina["datum"], y=kraj_vysocina["prirastok"], name="Vysočina"),row=5, col=2)
    fig.add_trace(go.Scatter(x=kraj_jihomoravsky["datum"], y=kraj_jihomoravsky["prirastok"], name="Jihomoravský"),row=6, col=1)
    fig.add_trace(go.Scatter(x=kraj_olomoucky["datum"], y=kraj_olomoucky["prirastok"], name="Olomoucký"),row=6, col=2)
    fig.add_trace(go.Scatter(x=kraj_zlinsky["datum"], y=kraj_zlinsky["prirastok"], name="Zlínsky"),row=7, col=1)
    fig.add_trace(go.Scatter(x=kraj_moravskoslezsky["datum"], y=kraj_moravskoslezsky["prirastok"], name="Moravskoslezský"),row=7, col=2)
    

    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_xaxes(title_text="Dátum", row=4, col=1)
    fig.update_xaxes(title_text="Dátum", row=5, col=1)
    fig.update_xaxes(title_text="Dátum", row=6, col=1)
    fig.update_xaxes(title_text="Dátum", row=7, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=4, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=5, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=6, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=7, col=1)

    fig.update_layout(height=1400, width=1300,  title=quartal_time+"pre denný prírastok incidencie na COVID pre jednotlivé kraje")

    fig.write_image(output_fig+"_prirastok.pdf")


    fig = make_subplots(rows=7, cols=2, subplot_titles=("Praha", "Stredočeský", "Jihočeský", "Plzenský", "Karlovarský", 
    "Ústecký", "Liberecký", "Kralovehradecký", "Pardubický", "Vysočina", "Jihomoravský", "Olomoucký", "Zlínsky", "Moravskoslezský"))

    fig.add_trace(go.Scatter(x=kraj_praha["datum"], y=kraj_praha["pocet_nakazenych_per_capita"], name="Praha"),row=1, col=1)
    fig.add_trace(go.Scatter(x=kraj_stredocesky["datum"], y=kraj_stredocesky["pocet_nakazenych_per_capita"], name="Stredočeský"),row=1, col=2)
    fig.add_trace(go.Scatter(x=kraj_jihocesky["datum"], y=kraj_jihocesky["pocet_nakazenych_per_capita"], name="Jihočeský"),row=2, col=1)
    fig.add_trace(go.Scatter(x=kraj_plzneksy["datum"], y=kraj_plzneksy["pocet_nakazenych_per_capita"], name="Plzenský"),row=2, col=2)
    fig.add_trace(go.Scatter(x=kraj_karlovarsky["datum"], y=kraj_karlovarsky["pocet_nakazenych_per_capita"], name="Karlovarský"),row=3, col=1)
    fig.add_trace(go.Scatter(x=kraj_ustecky["datum"], y=kraj_ustecky["pocet_nakazenych_per_capita"], name="Ústecký"),row=3, col=2)
    fig.add_trace(go.Scatter(x=kraj_liberecky["datum"], y=kraj_liberecky["pocet_nakazenych_per_capita"], name="Liberecký"),row=4, col=1)
    fig.add_trace(go.Scatter(x=kraj_kralovehradecky["datum"], y=kraj_kralovehradecky["pocet_nakazenych_per_capita"], name="Kralovehradecký"),row=4, col=2)
    fig.add_trace(go.Scatter(x=kraj_pardubicky["datum"], y=kraj_pardubicky["pocet_nakazenych_per_capita"], name="Pardubický"),row=5, col=1)
    fig.add_trace(go.Scatter(x=kraj_vysocina["datum"], y=kraj_vysocina["pocet_nakazenych_per_capita"], name="Vysočina"),row=5, col=2)
    fig.add_trace(go.Scatter(x=kraj_jihomoravsky["datum"], y=kraj_jihomoravsky["pocet_nakazenych_per_capita"], name="Jihomoravský"),row=6, col=1)
    fig.add_trace(go.Scatter(x=kraj_olomoucky["datum"], y=kraj_olomoucky["pocet_nakazenych_per_capita"], name="Olomoucký"),row=6, col=2)
    fig.add_trace(go.Scatter(x=kraj_zlinsky["datum"], y=kraj_zlinsky["pocet_nakazenych_per_capita"], name="Zlínsky"),row=7, col=1)
    fig.add_trace(go.Scatter(x=kraj_moravskoslezsky["datum"], y=kraj_moravskoslezsky["pocet_nakazenych_per_capita"], name="Moravskoslezský"),row=7, col=2)
    

    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_xaxes(title_text="Dátum", row=4, col=1)
    fig.update_xaxes(title_text="Dátum", row=5, col=1)
    fig.update_xaxes(title_text="Dátum", row=6, col=1)
    fig.update_xaxes(title_text="Dátum", row=7, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=4, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=5, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=6, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=7, col=1)

    fig.update_layout(height=1400, width=1300,  title=quartal_time+"prípadov na COVID prepočítaný na jedneho obyvateľa (per capita) pre jednotlivé kraje")

    fig.write_image(output_fig+"_per_capita.pdf")
    

    fig = make_subplots(rows=7, cols=2, subplot_titles=("Praha", "Stredočeský", "Jihočeský", "Plzenský", "Karlovarský", 
    "Ústecký", "Liberecký", "Kralovehradecký", "Pardubický", "Vysočina", "Jihomoravský", "Olomoucký", "Zlínsky", "Moravskoslezský"))

    fig.add_trace(go.Scatter(x=kraj_praha["datum"], y=kraj_praha["celkovy_pocet_obyvatelov"], name="Praha celkový počet obyvateľov"),row=1, col=1)
    fig.add_trace(go.Bar(x=kraj_praha["datum"], y=kraj_praha["celkovy_pocet_nakazenych"], name="Praha kumulatívny počet nakazených"),row=1, col=1)

    fig.add_trace(go.Scatter(x=kraj_stredocesky["datum"], y=kraj_stredocesky["celkovy_pocet_obyvatelov"], name="Stredočeský celkový počet obyvateľov"),row=1, col=2)
    fig.add_trace(go.Bar(x=kraj_stredocesky["datum"], y=kraj_stredocesky["celkovy_pocet_nakazenych"], name="Stredočeský kumulatívny počet nakazených"),row=1, col=2)

    fig.add_trace(go.Scatter(x=kraj_jihocesky["datum"], y=kraj_jihocesky["celkovy_pocet_obyvatelov"], name="Jihočeský celkový počet obyvateľov"),row=2, col=1)
    fig.add_trace(go.Bar(x=kraj_jihocesky["datum"], y=kraj_jihocesky["celkovy_pocet_nakazenych"], name="Jihočeský kumulatívny počet nakazených"),row=2, col=1)

    fig.add_trace(go.Scatter(x=kraj_plzneksy["datum"], y=kraj_plzneksy["celkovy_pocet_obyvatelov"], name="Plzenský celkový počet obyvateľov"),row=2, col=2)
    fig.add_trace(go.Bar(x=kraj_plzneksy["datum"], y=kraj_plzneksy["celkovy_pocet_nakazenych"], name="Plzenský kumulatívny počet nakazených"),row=2, col=2)

    fig.add_trace(go.Scatter(x=kraj_karlovarsky["datum"], y=kraj_karlovarsky["celkovy_pocet_obyvatelov"], name="Karlovarský celkový počet obyvateľov"),row=3, col=1)
    fig.add_trace(go.Bar(x=kraj_karlovarsky["datum"], y=kraj_karlovarsky["celkovy_pocet_nakazenych"], name="Karlovarský kumulatívny počet nakazených"),row=3, col=1)

    fig.add_trace(go.Scatter(x=kraj_ustecky["datum"], y=kraj_ustecky["celkovy_pocet_obyvatelov"], name="Ústecký celkový počet obyvateľov"),row=3, col=2)
    fig.add_trace(go.Bar(x=kraj_ustecky["datum"], y=kraj_ustecky["celkovy_pocet_nakazenych"], name="Ústecký kumulatívny počet nakazených"),row=3, col=2)

    fig.add_trace(go.Scatter(x=kraj_liberecky["datum"], y=kraj_liberecky["celkovy_pocet_obyvatelov"], name="Liberecký celkový počet obyvateľov"),row=4, col=1)
    fig.add_trace(go.Bar(x=kraj_liberecky["datum"], y=kraj_liberecky["celkovy_pocet_nakazenych"], name="Liberecký kumulatívny počet nakazených"),row=4, col=1)

    fig.add_trace(go.Scatter(x=kraj_kralovehradecky["datum"], y=kraj_kralovehradecky["celkovy_pocet_obyvatelov"], name="Kralovehradecký celkový počet obyvateľov"),row=4, col=2)
    fig.add_trace(go.Bar(x=kraj_kralovehradecky["datum"], y=kraj_kralovehradecky["celkovy_pocet_nakazenych"], name="Kralovehradecký kumulatívny počet nakazených"),row=4, col=2)

    fig.add_trace(go.Scatter(x=kraj_pardubicky["datum"], y=kraj_pardubicky["celkovy_pocet_obyvatelov"], name="Pardubický celkový počet obyvateľov"),row=5, col=1)
    fig.add_trace(go.Bar(x=kraj_pardubicky["datum"], y=kraj_pardubicky["celkovy_pocet_nakazenych"], name="Pardubický kumulatívny počet nakazených"),row=5, col=1)

    fig.add_trace(go.Scatter(x=kraj_vysocina["datum"], y=kraj_vysocina["celkovy_pocet_obyvatelov"], name="Vysočina celkový počet obyvateľov"),row=5, col=2)
    fig.add_trace(go.Bar(x=kraj_vysocina["datum"], y=kraj_vysocina["celkovy_pocet_nakazenych"], name="Vysočina kumulatívny počet nakazených"),row=5, col=2)

    fig.add_trace(go.Scatter(x=kraj_jihomoravsky["datum"], y=kraj_jihomoravsky["celkovy_pocet_obyvatelov"], name="Jihomoravský celkový počet obyvateľov"),row=6, col=1)
    fig.add_trace(go.Bar(x=kraj_jihomoravsky["datum"], y=kraj_jihomoravsky["celkovy_pocet_nakazenych"], name="Jihomoravský kumulatívny počet nakazených"),row=6, col=1)

    fig.add_trace(go.Scatter(x=kraj_olomoucky["datum"], y=kraj_olomoucky["celkovy_pocet_obyvatelov"], name="Olomoucký celkový počet obyvateľov"),row=6, col=2)
    fig.add_trace(go.Bar(x=kraj_olomoucky["datum"], y=kraj_olomoucky["celkovy_pocet_nakazenych"], name="Olomoucký kumulatívny počet nakazených"),row=6, col=2)

    fig.add_trace(go.Scatter(x=kraj_zlinsky["datum"], y=kraj_zlinsky["celkovy_pocet_obyvatelov"], name="Zlínsky celkový počet obyvateľov"),row=7, col=1)
    fig.add_trace(go.Bar(x=kraj_zlinsky["datum"], y=kraj_zlinsky["celkovy_pocet_nakazenych"], name="Zlínsky kumulatívny počet nakazených"),row=7, col=1)

    fig.add_trace(go.Scatter(x=kraj_moravskoslezsky["datum"], y=kraj_moravskoslezsky["celkovy_pocet_obyvatelov"], name="Moravskoslezský celkový počet obyvateľov"),row=7, col=2)
    fig.add_trace(go.Bar(x=kraj_moravskoslezsky["datum"], y=kraj_moravskoslezsky["celkovy_pocet_nakazenych"], name="Moravskoslezský kumulatívny počet nakazených"),row=7, col=2)


    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_xaxes(title_text="Dátum", row=4, col=1)
    fig.update_xaxes(title_text="Dátum", row=5, col=1)
    fig.update_xaxes(title_text="Dátum", row=6, col=1)
    fig.update_xaxes(title_text="Dátum", row=7, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=4, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=5, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=6, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=7, col=1)

    fig.update_layout(height=1400, width=1300,  title=quartal_time+"zobrazujúci celkový počet obyvateľov a kumulatívne prírastky na ochorenie COVID pre jednotlivé kraje")

    fig.write_image(output_fig+"_celkovy_pocet.pdf")

################################################################################################

def plot_graph_task2_deaths_line(name, output_fig, title, range="", range_set=False):
    data = pd.read_csv(name)

    fig = make_subplots(rows=3, cols=2, subplot_titles=("Celkový počet", "Neočkovani", "Po jednej dávke", "Očkovaní", "Očkovani vs Neočkovaní","Očkovaní x Po jednej dávke x Neočkovaní"))

    if range_set:
        data = data[(data['datum'] > range)]
        
        fig.add_trace(go.Scatter(x=data["datum"], y=data["umrti_celkom"], name="úmrtí celkom"),row=1, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)
        
        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)


    else:
        
        fig.add_trace(go.Scatter(x=data["datum"], y=data["umrti_celkom"], name="úmrtí celkom"),row=1, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["umrti_celkom"], name="úmrtí celkom"),row=3, col=2)

    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)

    fig.update_layout(height=1000, width=1000,  title=title)

    fig.write_image(output_fig+".pdf")


def plot_graph_task2_deaths_bar(name, output_fig, title, range="", range_set=False):
    data = pd.read_csv(name)

    fig = make_subplots(rows=4, cols=2, subplot_titles=("Celkový počet", "Neočkovani", "Po jednej dávke", "Očkovaní", "Očkovani vs Neočkovaní","Očkovaní x Po jednej dávke x Neočkovaní"))

    if range_set:
        data = data[(data['datum'] > range)]

        fig.add_trace(go.Bar(x=data["datum"], y=data["umrti_celkom"], name="úmrtí celkom"),row=1, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)


    else:
        fig.add_trace(go.Bar(x=data["datum"], y=data["umrti_celkom"], name="úmrtí celkom"),row=1, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["umrti_celkom"], name="úmrtí celkom"),row=3, col=2)

    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)

    fig.update_layout(height=1000, width=1000,  title=title, barmode='stack')

    fig.write_image(output_fig+".pdf")




def plot_graph_task2_hospit_line(name, output_fig, title, range="", range_set=False):
    data = pd.read_csv(name)

    fig = make_subplots(rows=3, cols=2, subplot_titles=("Celkový počet", "Neočkovani", "Po jednej dávke", "Očkovaní", "Očkovani vs Neočkovaní", "Očkovaní x Po jednej dávke x Neočkovaní"))
    
    if range_set:
        data = data[(data['datum'] > range)]
        
        fig.add_trace(go.Scatter(x=data["datum"], y=data["hospitalizovani_celkom"], name="hospitalizácií celkom"),row=1, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)

    else:
       
        fig.add_trace(go.Scatter(x=data["datum"], y=data["hospitalizovani_celkom"], name="hospitalizácií celkom"),row=1, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)

        fig.add_trace(go.Scatter(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)
        fig.add_trace(go.Scatter(x=data["datum"], y=data["hospitalizovani_celkom"], name="hospitalizácií celkom"),row=3, col=2)

    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)

    fig.update_layout(height=1000, width=1000,  title=title)

    fig.write_image(output_fig+".pdf")




def plot_graph_task2_hospit_bar(name, output_fig, title, range="", range_set=False):
    data = pd.read_csv(name)

    fig = make_subplots(rows=3, cols=2, subplot_titles=("Celkový počet", "Neočkovani", "Po jednej dávke", "Očkovaní", "Očkovani vs Neočkovaní", "Očkovaní x Po jednej dávke x Neočkovaní"))

    if range_set:
        data = data[(data['datum'] > range)]
        
        fig.add_trace(go.Bar(x=data["datum"], y=data["hospitalizovani_celkom"], name="hospitalizácií celkom"),row=1, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)
        
        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)

    else:
        
        fig.add_trace(go.Bar(x=data["datum"], y=data["hospitalizovani_celkom"], name="hospitalizácií celkom"),row=1, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=1, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=2, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=2, col=2)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=1)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=1)

        fig.add_trace(go.Bar(x=data["datum"], y=data["neockovani"], name="neočkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["zaockovani"], name="očkovaní"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["jedna_davka"], name="jedna dávka"),row=3, col=2)
        fig.add_trace(go.Bar(x=data["datum"], y=data["hospitalizovani_celkom"], name="hospitalizácií celkom"),row=3, col=2)

    fig.update_xaxes(title_text="Dátum", row=1, col=1)
    fig.update_xaxes(title_text="Dátum", row=2, col=1)
    fig.update_xaxes(title_text="Dátum", row=3, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=1, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=2, col=1)
    fig.update_yaxes(title_text="Počet ľudí", row=3, col=1)

    fig.update_layout(height=1000, width=1000,  title=title, barmode='stack')

    fig.write_image(output_fig+".pdf")