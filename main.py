import DataRefiner
import PM_Traffic_Dataholder
import RF_Regression

import finedust_ship as ship

from tkinter import *
from PIL import Image


class MyFrame(Frame):
    def __init__(self, master):
        master.geometry("800x600+100+100")
        Frame.__init__(self, master)

        self.master = master
        self.master.title("부산 미세먼지 분석 - 학부생 프로젝트")
        self.pack(fill=BOTH, expand=True)

        self.frame_main = Frame(self)

        self.first_window_frame()

    def first_window_frame(self):
        # 분석 선택
        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack()

        lblSelect = Label(self.frame_main, text="분석을 선택하세요", width=40)
        lblSelect.pack(pady=30)

        btn_traffic = Button(self.frame_main, text="교통량과 미세먼지 분석", command=self.click_traffic)
        btn_traffic.pack(padx=10, pady=10)

        btn_ship = Button(self.frame_main, text="항만과 미세먼지 분석", command=self.click_ship)
        btn_ship.pack(padx=10, pady=10)

        btn_finish = Button(self.frame_main, text="종료하기",command=self.finish_program)
        btn_finish.pack(padx=10, pady=40)

    def click_traffic(self):
        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack()

        # 교통량
        lblSelect = Label(self.frame_main, text="교통량 데이터와 기상 데이터를 함께 분석하시겠습니까?")
        lblSelect.pack(pady=30)

        frame_btn = Frame(self.frame_main)
        frame_btn.pack()

        btn_yes = Button(frame_btn, text="예", command=self.traffic_with_weather)
        btn_yes.pack(side=LEFT, padx=20)
        btn_no = Button(frame_btn, text="아니요", command=self.traffic_without_weather)
        btn_no.pack(side=RIGHT, padx=20)

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=30)

    def traffic_with_weather(self):
        self.please_wait()

        dataholder = PM_Traffic_Dataholder.DataHolder()
        target, data, names, batchnum, dim = dataholder.get_Weather_Traffic()
        regressor = RF_Regression.RF_Regressor(target=target, data=data, names=names)
        result_mse, result_RF, result_corr = regressor.RF(batch=batchnum, dim=dim)

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack()

        frame_values = Frame(self.frame_main)
        frame_values.pack()

        lbl_mse = Label(frame_values, text=result_mse)
        lbl_mse.pack(padx=10)

        lbl_rf = Label(frame_values, text=result_RF)
        lbl_rf.pack(padx=10)

        lbl_corr = Label(frame_values, text=result_corr)
        lbl_corr.pack(padx=10)

        frame_btn = Frame(self.frame_main)
        frame_btn.pack()

        frame_graph = Frame(self.frame_main)
        frame_graph.pack()

        img_tree_img = PhotoImage(file='traffic_tree_number_plot.png')
        lbl_tree_img = Label(frame_graph, image=img_tree_img)
        lbl_tree_img.image = img_tree_img  # 레퍼런스 추가
        lbl_tree_img.pack()

        img_feat_img = PhotoImage(file='traffic_feature_importance.png')
        lbl_feat_img = Label(frame_graph, image=img_feat_img)
        lbl_feat_img.image = img_feat_img  # 레퍼런스 추가
        lbl_feat_img.pack()

        img_pearson_img = PhotoImage(file='traffic_pearson_coefficient.png')
        lbl_pearson_img = Label(frame_graph, image=img_pearson_img)
        lbl_pearson_img.image = img_pearson_img  # 레퍼런스 추가
        lbl_pearson_img.pack()

        btn_tree = Button(frame_btn, text="Number of Trees in Ensemble",
                          command=lambda: self.select_region_traffic_graph(lbl_tree_img))
        btn_tree.pack(side=LEFT, padx=5)

        btn_feat = Button(frame_btn, text="Variable Importance",
                          command=lambda: self.select_region_traffic_graph(lbl_feat_img))
        btn_feat.pack(side=LEFT, padx=5)

        btn_pearson = Button(frame_btn, text="Pearson Coefficient",
                             command=lambda: self.select_region_traffic_graph(lbl_pearson_img))
        btn_pearson.pack(side=LEFT, padx=5)

        lbl_tree_img.pack_forget()
        lbl_feat_img.pack_forget()
        lbl_pearson_img.pack_forget()

        self.curpack_traffic_graph = lbl_tree_img

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack()

    def traffic_without_weather(self):
        self.please_wait()

        dataholder = PM_Traffic_Dataholder.DataHolder()
        target, data, names, batchnum, dim = dataholder.get_Traffic_PM()
        regressor = RF_Regression.RF_Regressor(target=target, data=data, names=names)
        result_mse, result_RF, result_corr = regressor.RF(batch=batchnum, dim=dim)

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack(pady=10)

        frame_values = Frame(self.frame_main)
        frame_values.pack(pady=5)

        lbl_mse = Label(frame_values, text=result_mse)
        lbl_mse.pack(side=LEFT,padx=10)

        lbl_rf = Label(frame_values, text=result_RF)
        lbl_rf.pack(side=LEFT,padx=10)

        lbl_corr = Label(frame_values, text=result_corr)
        lbl_corr.pack(side=LEFT,padx=10)

        frame_btn = Frame(self.frame_main)
        frame_btn.pack()

        frame_graph = Frame(self.frame_main)
        frame_graph.pack()

        img_tree_img = PhotoImage(file='traffic_tree_number_plot.png')
        lbl_tree_img = Label(frame_graph, image=img_tree_img)
        lbl_tree_img.image = img_tree_img  # 레퍼런스 추가
        lbl_tree_img.pack()

        img_feat_img = PhotoImage(file='traffic_feature_importance.png')
        lbl_feat_img = Label(frame_graph, image=img_feat_img)
        lbl_feat_img.image = img_feat_img  # 레퍼런스 추가
        lbl_feat_img.pack()

        img_pearson_img = PhotoImage(file='traffic_pearson_coefficient.png')
        lbl_pearson_img = Label(frame_graph, image=img_pearson_img)
        lbl_pearson_img.image = img_pearson_img  # 레퍼런스 추가
        lbl_pearson_img.pack()

        btn_tree = Button(frame_btn, text="Number of Trees in Ensemble", command=lambda: self.select_region_traffic_graph(lbl_tree_img))
        btn_tree.pack(side=LEFT,padx=5)

        btn_feat = Button(frame_btn, text="Variable Importance", command=lambda: self.select_region_traffic_graph(lbl_feat_img))
        btn_feat.pack(side=LEFT,padx=5)

        btn_pearson = Button(frame_btn, text="Pearson Coefficient", command=lambda: self.select_region_traffic_graph(lbl_pearson_img))
        btn_pearson.pack(side=LEFT,padx=5)

        lbl_tree_img.pack_forget()
        lbl_feat_img.pack_forget()
        lbl_pearson_img.pack_forget()

        self.curpack_traffic_graph = lbl_tree_img

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack()

    def select_region_traffic_graph(self, label):
        self.curpack_traffic_graph.pack_forget()
        self.curpack_traffic_graph = label
        label.pack()


    def click_ship(self):
        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack(pady=30)

        # 항만
        btn_get_map = Button(self.frame_main, text="2014~2016년 부산 지역별 평균 미세먼지 지도", command=self.ship_get_map)
        btn_get_map.pack(padx=10, pady=10)

        btn_with_wind = Button(self.frame_main, text="부산항에서의 풍향에 따른 타지역의 미세먼지 변화 분석",
                               command=self.ship_pm10_according_to_windASOS)
        btn_with_wind.pack(padx=10, pady=10)

        btn_with_pusanport_ship_traffic = Button(self.frame_main, text="부산항 컨테이너 물동량에 따른 미세먼지 분석",
                                                 command=self.ship_pm10_according_to_traffic)
        btn_with_pusanport_ship_traffic.pack(padx=10, pady=10)

        btn_with_newport_ship_traffic = Button(self.frame_main, text="부산신항 컨테이너 물동량에 따른 미세먼지 분석",
                                                 command=self.ship_pm10_according_to_traffic_sinhang)
        btn_with_newport_ship_traffic.pack(padx=10, pady=10)

        btn_specific_month = Button(self.frame_main, text="1,2,3 월 태종대와 광복동 미세먼지 변화",
                                               command=self.ship_compare_specific_month)
        btn_specific_month.pack(padx=10, pady=10)

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=30)

    def ship_get_map(self):
        self.please_wait()

        station, value = ship.get_map()

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack()

        title = "\n\n2014~2016 year average fine dust each station\n"
        lblstr = Label(self.frame_main, text=title)
        lblstr.pack()

        frame_table = Frame(self.frame_main)
        frame_table.pack()
        lblstation = Label(frame_table, text=station)
        lblstation.pack(side=LEFT)
        lblvalue = Label(frame_table, text=value)
        lblvalue.pack(side=LEFT, padx=20)

        img = PhotoImage(file='2014_2016_year_aver_dust.gif')
        lblimage = Label(frame_table, image=img)
        lblimage.image = img  # 레퍼런스 추가
        lblimage.pack(side=LEFT, padx=20)

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=10)

    def ship_pm10_according_to_windASOS(self):
        self.please_wait()

        gwangan, daesin, hakjang, soojung, busanjin, busanjin2014, busanjin2015, busanjin2016 = ship.pm10_according_to_windASOS()

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack(pady=30)

        frame_content = Frame(self.frame_main)
        frame_content.pack()

        frame_menu = Frame(frame_content)
        frame_menu.pack(side=LEFT, padx=10)

        frame_desc = Frame(frame_content)
        frame_desc.pack(side=LEFT, padx=10)

        lblgwangan = Label(frame_desc, text=gwangan)
        lblgwangan.pack()
        lbldaesin = Label(frame_desc, text=daesin)
        lbldaesin.pack()
        lblhakjang = Label(frame_desc, text=hakjang)
        lblhakjang.pack()
        lblsoojung = Label(frame_desc, text=soojung)
        lblsoojung.pack()
        lblbusanjin = Label(frame_desc, text=busanjin)
        lblbusanjin.pack()

        lblbusanjin2014 = Label(frame_desc, text=busanjin2014)
        lblbusanjin2014.pack()
        lblbusanjin2015 = Label(frame_desc, text=busanjin2015)
        lblbusanjin2015.pack()
        lblbusanjin2016 = Label(frame_desc, text=busanjin2016)
        lblbusanjin2016.pack()

        lblgwangan.pack_forget()
        lbldaesin.pack_forget()
        lblhakjang.pack_forget()
        lblsoojung.pack_forget()
        lblbusanjin.pack_forget()

        lblbusanjin2014.pack_forget()
        lblbusanjin2015.pack_forget()
        lblbusanjin2016.pack_forget()

        self.curpack_windASOS = lblgwangan

        btn_gwangan = Button(frame_menu, text="부산항의 풍향이 광안동 방향인 경우", command=lambda: self.select_region_windASOS(lblgwangan))
        btn_gwangan.pack(pady=10)
        btn_daesin = Button(frame_menu, text="부산항의 풍향이 대신동 방향인 경우", command=lambda: self.select_region_windASOS(lbldaesin))
        btn_daesin.pack(pady=10)
        btn_hakjang = Button(frame_menu, text="부산항의 풍향이 학장동 방향인 경우", command=lambda: self.select_region_windASOS(lblhakjang))
        btn_hakjang.pack(pady=10)
        btn_soojung = Button(frame_menu, text="부산항의 풍향이 수정동 방향인 경우", command=lambda: self.select_region_windASOS(lblsoojung))
        btn_soojung.pack(pady=10)
        btn_busangjin = Button(frame_menu, text="부산항의 풍향이 부산진 방향인 경우", command=lambda: self.select_region_windASOS(lblbusanjin))
        btn_busangjin.pack(pady=10)

        btn_busangjin2014 = Button(frame_menu, text="부산항의 풍향이 부산진 방향, 2014년", command=lambda: self.select_region_windASOS(lblbusanjin2014))
        btn_busangjin2014.pack(pady=10)
        btn_busangjin2015 = Button(frame_menu, text="부산항의 풍향이 부산진 방향, 2015년", command=lambda: self.select_region_windASOS(lblbusanjin2015))
        btn_busangjin2015.pack(pady=10)
        btn_busangjin2016 = Button(frame_menu, text="부산항의 풍향이 부산진 방향, 2016년", command=lambda: self.select_region_windASOS(lblbusanjin2016))
        btn_busangjin2016.pack(pady=10)

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=10)

    def select_region_windASOS(self, label):
        self.curpack_windASOS.pack_forget()
        self.curpack_windASOS = label
        label.pack()

    def ship_pm10_according_to_traffic(self):
        self.please_wait()

        return_all_station_ship, return_all_station_container, return_teajongdea_ship, return_teajongdea_container, \
        return_gwangbok_ship, return_gwangbok_container, return_teajongdea_ship2014, return_teajongdea_container2014, \
        return_gwangbok_ship2014, return_gwangbok_container2014, return_teajongdea_ship2015, return_teajongdea_container2015, \
        return_gwangbok_ship2015, return_gwangbok_container2015, return_teajongdea_ship2016, return_teajongdea_container2016, \
        return_gwangbok_ship2016, return_gwangbok_container2016 = ship.pm10_according_to_traffic()

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack(pady=30)

        frame_content = Frame(self.frame_main)
        frame_content.pack()

        frame_menu = Frame(frame_content)
        frame_menu.pack(side=LEFT, padx=20)

        frame_desc = Frame(frame_content)
        frame_desc.pack(side=LEFT, padx=20)

        # label

        lbl_all_station = Label(frame_desc, text=return_all_station_ship + '\n\n' + return_all_station_container)
        lbl_all_station.pack()

        lbl_teajongdea = Label(frame_desc, text=return_teajongdea_ship + '\n\n' + return_teajongdea_container)
        lbl_teajongdea.pack()

        lbl_teajongdea2016 = Label(frame_desc, text=return_teajongdea_ship2016 + '\n\n' + return_teajongdea_container2016)
        lbl_teajongdea2016.pack()

        lbl_teajongdea2015 = Label(frame_desc, text=return_teajongdea_ship2015 + '\n\n' + return_teajongdea_container2015)
        lbl_teajongdea2015.pack()

        lbl_teajongdea2014 = Label(frame_desc, text=return_teajongdea_ship2014 + '\n\n' + return_teajongdea_container2014)
        lbl_teajongdea2014.pack()

        lbl_gwangbok = Label(frame_desc, text=return_gwangbok_ship + '\n\n' + return_gwangbok_container)
        lbl_gwangbok.pack()

        lbl_gwangbok2016 = Label(frame_desc, text=return_gwangbok_ship2016 + '\n\n' + return_gwangbok_container2016)
        lbl_gwangbok2016.pack()

        lbl_gwangbok2015 = Label(frame_desc, text=return_gwangbok_ship2015 + '\n\n' + return_gwangbok_container2015)
        lbl_gwangbok2015.pack()

        lbl_gwangbok2014 = Label(frame_desc, text=return_gwangbok_ship2014 + '\n\n' + return_gwangbok_container2014)
        lbl_gwangbok2014.pack()

        # button

        btn_all_station = Button(frame_menu, text="부산 전체 측정소 평균", command=lambda: self.select_region_ship_traffic(lbl_all_station))
        btn_all_station.pack(pady = 10)

        btn_teajongdea = Button(frame_menu, text="영도구 태종대 2014~2016 년 평균", command=lambda: self.select_region_ship_traffic(lbl_teajongdea))
        btn_teajongdea.pack(pady = 10)

        btn_teajongdea2016 = Button(frame_menu, text="영도구 태종대 2016 년", command=lambda: self.select_region_ship_traffic(lbl_teajongdea2016))
        btn_teajongdea2016.pack(pady = 10)

        btn_teajongdea2015 = Button(frame_menu, text="영도구 태종대 2015 년", command=lambda: self.select_region_ship_traffic(lbl_teajongdea2015))
        btn_teajongdea2015.pack(pady = 10)

        btn_teajongdea2014 = Button(frame_menu, text="영도구 태종대 2014 년", command=lambda: self.select_region_ship_traffic(lbl_teajongdea2014))
        btn_teajongdea2014.pack(pady = 10)

        btn_gwangbok = Button(frame_menu, text="중구 광복동 2014~2016 년 평균", command=lambda: self.select_region_ship_traffic(lbl_gwangbok))
        btn_gwangbok.pack(pady = 10)

        btn_gwangbok2016 = Button(frame_menu, text="중구 광복동 2016 년", command=lambda: self.select_region_ship_traffic(lbl_gwangbok2016))
        btn_gwangbok2016.pack(pady = 10)

        btn_gwangbok2015 = Button(frame_menu, text="중구 광복동 2015 년", command=lambda: self.select_region_ship_traffic(lbl_gwangbok2015))
        btn_gwangbok2015.pack(pady = 10)

        btn_gwangbok2014 = Button(frame_menu, text="중구 광복동 2014 년", command=lambda: self.select_region_ship_traffic(lbl_gwangbok2014))
        btn_gwangbok2014.pack(pady = 10)

        lbl_all_station.pack_forget()
        lbl_teajongdea.pack_forget()
        lbl_teajongdea2016.pack_forget()
        lbl_teajongdea2015.pack_forget()
        lbl_teajongdea2014.pack_forget()
        lbl_gwangbok.pack_forget()
        lbl_gwangbok2016.pack_forget()
        lbl_gwangbok2015.pack_forget()
        lbl_gwangbok2014.pack_forget()

        self.curpack_ship_traffic = lbl_all_station

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=10)

    def select_region_ship_traffic(self, label):
        self.curpack_ship_traffic.pack_forget()
        self.curpack_ship_traffic = label
        label.pack()

    def ship_pm10_according_to_traffic_sinhang(self):
        self.please_wait()

        return_all_station_container, return_all_station_ship, return_noksan_container, return_noksan_ship = ship.pm10_according_to_traffic_sinhang()

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack(pady=30)

        frame_content = Frame(self.frame_main)
        frame_content.pack(pady= 40)

        frame_menu = Frame(frame_content)
        frame_menu.pack(side=LEFT, padx=10)

        frame_desc = Frame(frame_content)
        frame_desc.pack(side=LEFT, padx=10)

        lbl_all_station = Label(frame_desc, text=return_all_station_ship + '\n\n' + return_all_station_container)
        lbl_all_station.pack()

        lbl_noksan = Label(frame_desc, text=return_noksan_ship + '\n\n' + return_noksan_container)
        lbl_noksan.pack()

        lbl_all_station.pack_forget()
        lbl_noksan.pack_forget()
        self.curpack_ship_traffic_sinhang = lbl_all_station

        btn_all_station = Button(frame_menu, text="부산 전체 측정소 평균", command=lambda: self.select_region_ship_traffic_sinhang(lbl_all_station))
        btn_all_station.pack(pady=20)
        btn_noksan = Button(frame_menu, text="강서구 녹산동 측정소", command=lambda: self.select_region_ship_traffic_sinhang(lbl_noksan))
        btn_noksan.pack(pady=20)

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=10)

    def select_region_ship_traffic_sinhang(self, label):
        self.curpack_ship_traffic_sinhang.pack_forget()
        self.curpack_ship_traffic_sinhang = label
        label.pack()

    def ship_compare_specific_month(self):
        self.please_wait()

        return_teajongdea, return_gwangbok = ship.compare_specific_month()

        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack(pady=30)

        frame_content = Frame(self.frame_main)
        frame_content.pack(pady=40)

        lbl_teajongdea = Label(frame_content, text=return_teajongdea)
        lbl_teajongdea.pack(side=LEFT, padx=20)

        line = ""
        for i in range(13):
            line += "|"
            if i < 12:
                line += "\n"
        lbl_line = Label(frame_content, text=line)
        lbl_line.pack(side=LEFT, padx=10)

        lbl_gwangbok = Label(frame_content, text=return_gwangbok)
        lbl_gwangbok.pack(side=LEFT, padx=20)

        btn_back = Button(self.frame_main, text="메인으로 돌아가기", command=self.first_window_frame)
        btn_back.pack(pady=10)


    def please_wait(self):
        self.frame_main.destroy()
        self.frame_main = Frame(self)
        self.frame_main.pack()

        lblwait = Label(self.frame_main, text="잠시만 기다려주세요")
        lblwait.pack(pady=30)

        self.master.update()

    def finish_program(self):
        self.master.destroy()


def main():
    root = Tk()
    app = MyFrame(root)
    root.mainloop()


if __name__ == '__main__':
    main()