import logging
import sys
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import csv


def proc_dri(log_obj, html, driver, soup1, year, mth, day, RaceNo, loc, syr):
    # while errFlag == False:
    soup = BeautifulSoup(html, "html.parser")
    temp = soup.find("td", {"colspan": "16"})
    if temp is not None:
        try:
            content = []
            RaceYr = year
            RaceMth = mth
            RaceDay = day
            RaceNum = RaceNo
            RaceLoc = loc
            date = str(RaceYr + RaceMth + RaceDay) + "-" + str(RaceNo)
            temp = temp.get_text().strip()
            temp1 = temp.split("(")
            temp2 = temp1[1].split(")")
            year1 = int(syr) + 1
            # RaceID = str(syr) + "-" + str(year1) + "-" + temp2[0] #identifer of Race (season + raceid)
            # RaceID = temp2[0]
            # log_obj.info('RaceID %s'.format(), RaceID)
            # print("RaceID: " + RaceID)
            temp = soup.find("td", {"style": "width: 385px;"})
            temp = temp.get_text()
            RaceClass = str(temp).split(" - ")[0]
            # print("Class " + RaceClass)
            RaceLenth = str(temp).split(" - ")[1]
            # print("Length " + RaceLenth)
            RaceGoing = soup.find("td", {"colspan": "14"}).get_text()
            # print("Going " + RaceGoing)
            RaceTrack = soup.find_all("td", {"colspan": "14"})[1].get_text()
            # print("Track: " + RaceTrack)
            TotalRaceTime = soup.find_all("td", {"style": "width:65px;"})
            i = 0
            raceTime = []
            while i < (len(TotalRaceTime)):
                temp = ""
                temp1 = ""
                temp = TotalRaceTime[i].getText().split("(")
                temp1 = temp[1].split(")")
                raceTime.append(temp1[0])
                temp = ""
                temp1 = ""
                i = i + 1
            print(raceTime)
            my_dict = {}
            log_obj.info("in dict".format())
            # headers = [header.text for header in soup.findAll('table')[2].find('tr', {'class': 'bg_blue color_w'}).find_all('td')]
            headers = [
                "Place",
                "Horse_No",
                "Horse_Name",
                "Jockey",
                "Trainer",
                "Actual_Weight",
                "Declare_Horse_Wt",
                "Draw",
                "LBW",
                "RunningPos1",
                "RunningPos2",
                "RunningPos3",
                "RunningPos4",
                "RunningPos5",
                "Finish_Time",
                "Win_Odds",
                "Class",
                "Loc",
                "Length",
                "Going",
                "Track",
                "Year",
                "Month",
                "Day",
                "RaceNo",
            ]
            resultTable = soup.findAll("table")[2].find_all("tr", {"class": None})
            # filename = RaceID + ".csv"
            filename = "result_2223_ST.csv"
            with open(
                "./data/" + filename, "a", newline="", encoding="big5hkscs"
            ) as csvfile:
                log_obj.info(
                    "Logging to csv: Date: %s - Race %s".format(), date, temp2[0]
                )
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                for vals in resultTable:
                    vals = [
                        i.text.replace("\n", "")
                        .replace("\xa0", "")
                        .replace("                                ", "")
                        .replace("                ", "")
                        .replace("            ", "")
                        .replace("        ", " ")
                        .split(" ")
                        for i in vals.find_all("td")
                    ]
                    my_dict.update(dict(zip(headers, vals)))
                    # my_dict.update({'RaceID': RaceID})
                    # Split RunningPos into 5 columns
                    my_dict.update({"RunningPos1": vals[9][1]})
                    my_dict.update({"RunningPos2": vals[9][2]})
                    my_dict.update({"RunningPos3": vals[9][3]})
                    try:
                        my_dict.update({"RunningPos4": vals[9][4]})
                    except Exception as e:
                        my_dict.update({"RunningPos4": ""})
                    try:
                        my_dict.update({"RunningPos5": vals[9][5]})
                    except Exception as e:
                        my_dict.update({"RunningPos5": ""})
                    my_dict.update({"Class": RaceClass})
                    my_dict.update({"Loc": RaceLoc})
                    my_dict.update({"Length": RaceLenth})
                    my_dict.update({"Going": RaceGoing})
                    my_dict.update({"Track": RaceTrack})
                    my_dict.update({"Year": year})
                    my_dict.update({"Month": mth})
                    my_dict.update({"Day": day})
                    my_dict.update({"RaceNo": temp2[0]})

                    # print(my_dict)
                    writer.writerow(my_dict)
                log_obj.info(
                    "Logging to csv: Date: %s - Race %s Done".format(),
                    date,
                    temp2[0],
                )
        except Exception as e:
            log_obj.critical("Error: Expection %s", exc_info=e)
            pass

    log_obj.info("Loop Finish")


def web(log_obj, link, year, mth, day, RaceNo, loc, syr):
    # race_season = year + "/" + year+1
    log_obj.info("Web Fetch Starts".format())

    # Old Driver code, Python version max 3.9
    # chrome_options = Options()
    # chrome_options.page_load_strategy = 'normal'
    # chrome_options.add_argument('--enable-automation')
    # chrome_options.add_argument('disable-infobars')
    # chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--lang=en')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--allow-insecure-localhost')
    # chrome_options.add_argument('--allow-running-insecure-content')
    # chrome_options.add_argument('--disable-notifications')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--disable-browser-side-navigation')
    # chrome_options.add_argument('--mute-audio')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--force-device-scale-factor=1')

    # chrome_options.add_experimental_option(
    #     'prefs', {
    #         'intl.accept_languages': 'en,en_US',
    #         'download.prompt_for_download': False,
    #         'download.default_directory': '/dev/null',
    #         'automatic_downloads': 2,
    #         'download_restrictions': 3,
    #         'notifications': 2,
    #         'media_stream': 2,
    #         'media_stream_mic': 2,
    #         'media_stream_camera': 2,
    #         'durable_storage': 2,
    #     }
    # )

    # service = Service(executable_path='geckodriver.exe')
    # driver = webdriver.Firefox(service=service, options=fireFoxOptions)
    # driver = webdriver.Firefox(executable_path='geckodriver.exe', options=fireFoxOptions);

    # Add additional Options to the webdriver
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("-headless")
    fireFoxOptions.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"

    # Chrome Drvier drive code
    # driver = webdriver.Chrome('chromedriver', options=chrome_options)
    # driver.set_page_load_timeout(10)  # Timeout 10 seconds

    # Firefox Driver drive code
    serv = Service("./geckodriver.exe")
    driver = webdriver.Firefox(service=serv, options=fireFoxOptions)
    driver.implicitly_wait(10)
    driver.set_page_load_timeout(10)
    # Add exception handling on timeout (10s)
    cnt = 0 # counter for timeout exception
    try:
        driver.get(link)
    except TimeoutException:
        cnt +=1
        log_obj.info("Timeout Exception, reloading " + str(cnt) + "/3 times, retrying...")
        if cnt < 3:
            time.sleep(5)
            driver.get(link)
        else:
            log_obj.error("Timeout Exception, reloaded "+ str(cnt) + "/3 times, stopping the program...")
            sys.exit(0)
    
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    driver.close()
    tempwebstr = str(soup.find_all("div", {"id": "errorContainer"})).strip()
    tempwebstr2 = str(soup.find_all("div", {"class": "race_tab"})).strip()
    print("tempwebstr" + str(tempwebstr.strip()))
    print("tempwebstr2" + str(tempwebstr2.strip()))
    log_obj.info("tempwebstr2 len = " + str(len(tempwebstr2.strip())).format())
    log_obj.info("tempwebstr len = " + str(len(tempwebstr.strip())).format())
    if len(str(tempwebstr)) > 2:  # err container exist = no race
        return False
    if len(str(tempwebstr2)) > 2:  # racetab exist = have race
        proc_dri(
            log_obj=log_obj,
            driver=driver,
            soup1=soup,
            html=html,
            year=year,
            mth=mth,
            day=day,
            RaceNo=RaceNo,
            loc=loc,
            syr=syr,
        )
        return True
    if len(tempwebstr) == 2 & len(tempwebstr2) == 2:
        return False


def main():
    file_name = "raceInfo_log"
    log_obj = Logger(file_name)

    grabbing = True
    # Fetch all race data from 2010/2011 - 2021/2022 (SHA TIN)
    syr = 23
    mth = 6
    day = 10
    num = 1
    loc = "ST"
    # loc = "HV"
    # link = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=2021/02/28"
    while grabbing == True:
        if day >= 1 and day <= 9:
            tempday = "0" + str(day)  # 1-9 should be 01-09
        else:
            tempday = str(day)

        if mth >= 1 and mth <= 9:
            tempmth = "0" + str(mth)  # 1-9 should be 01 - 09
        else:
            tempmth = mth
        year = "20" + str(syr)
        log_obj.info("Cur Race" + str(num))
        log_obj.info("Cur Date: " + str(year) + "/" + str(tempmth) + "/" + str(tempday))

        # link = 'https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate=' + str(year) + '/' + str(tempmth) + '/'+ str(tempday) + "&Racecourse=" + str(loc) + "&RaceNo=" + str(num)
        link = (
            "https://racing.hkjc.com/racing/information/Chinese/Racing/LocalResults.aspx?RaceDate="
            + str(year)
            + "/"
            + str(tempmth)
            + "/"
            + str(tempday)
            + "&Racecourse="
            + str(loc)
            + "&RaceNo="
            + str(num)
        )
        log_obj.info("Link: %s", link)
        result = web(
            log_obj=log_obj,
            link=link,
            year=str(year),
            mth=str(mth),
            day=str(day),
            RaceNo=str(num),
            loc=str(loc),
            syr=str(syr),
        )

        if day == 31 and mth == 12:
            syr += 1
            day = 0
            mth = 1
            num = 1
            log_obj.info("Year end, switching to next yr...")
            log_obj.info("Next Race" + str(num))
            log_obj.info("Next Date: " + str(syr) + "/" + str(mth) + "/" + str(day))
            log_obj.info(
                "Next Long Date: " + str(year) + "/" + str(tempmth) + "/" + str(tempday)
            )

        if result == False:
            log_obj.info("result == False, No race found, passing...")
            num = 1
            day += 1
            if day == 32:
                mth += 1
                day = 1
            if mth == 13:
                syr += 1
                mth = 1
                day = 1

        if result == True:
            log_obj.info("result == True, Race found, recording...")
            num += 1
            if day == 31 and num == 12:
                day = 1
                mth += 1
                num = 1
            if num == 12:
                day += 1
                num = 0


def Logger(file_name):
    formatter = logging.Formatter(
        fmt="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
    )  # %I:%M:%S %p AM|PM format
    logging.basicConfig(
        filename="%s.log" % (file_name),
        format="%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s",
        datefmt="%Y/%m/%d %H:%M:%S",
        filemode="w",
        level=logging.INFO,
    )
    log_obj = logging.getLogger()
    log_obj.setLevel(logging.INFO)
    # log_obj = logging.getLogger().addHandler(logging.StreamHandler())

    # console printer
    screen_handler = logging.StreamHandler(
        stream=sys.stdout
    )  # stream=sys.stdout is similar to normal print
    screen_handler.setFormatter(formatter)
    logging.getLogger().addHandler(screen_handler)

    log_obj.info("Logger object created successfully..")
    return log_obj


if __name__ == "__main__":
    main()
