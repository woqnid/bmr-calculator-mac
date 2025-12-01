#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
import math

class BMRCalculator:
    def __init__(self, root):
        self.root = root
        self.setup_ui()
    
    def setup_ui(self):
        self.root.title("BMR计算器 - macOS版")
        self.root.geometry("500x650")
        self.root.resizable(True, True)
        
        # 主框架
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text="BMR/TDEE 计算器", 
            font=("Helvetica", 16, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 输入框架
        input_frame = ttk.LabelFrame(main_frame, text="个人信息", padding="15")
        input_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(1, weight=1)
        
        # 体重输入
        ttk.Label(input_frame, text="体重 (kg):").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.weight_var = tk.StringVar(value="65")
        weight_entry = ttk.Entry(input_frame, textvariable=self.weight_var)
        weight_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # 身高输入
        ttk.Label(input_frame, text="身高 (cm):").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.height_var = tk.StringVar(value="170")
        height_entry = ttk.Entry(input_frame, textvariable=self.height_var)
        height_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # 年龄输入
        ttk.Label(input_frame, text="年龄:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.age_var = tk.StringVar(value="30")
        age_entry = ttk.Entry(input_frame, textvariable=self.age_var)
        age_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        
        # 性别选择
        ttk.Label(input_frame, text="性别:").grid(row=3, column=0, sticky=tk.W, pady=8)
        gender_frame = ttk.Frame(input_frame)
        gender_frame.grid(row=3, column=1, sticky=tk.W, pady=8, padx=(10, 0))
        self.gender_var = tk.StringVar(value="男")
        ttk.Radiobutton(gender_frame, text="男", variable=self.gender_var, value="男").pack(side=tk.LEFT, padx=(0, 10))
        ttk.Radiobutton(gender_frame, text="女", variable=self.gender_var, value="女").pack(side=tk.LEFT)
        
        # 活动水平
        ttk.Label(input_frame, text="活动水平:").grid(row=4, column=0, sticky=tk.W, pady=8)
        self.activity_var = tk.StringVar()
        activity_combo = ttk.Combobox(input_frame, textvariable=self.activity_var, state="readonly")
        activity_combo['values'] = ('久坐', '轻度活动', '中度活动', '重度活动', '极重度活动')
        activity_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=8, padx=(10, 0))
        activity_combo.current(2)
        
        # 计算按钮
        calculate_btn = ttk.Button(main_frame, text="计算 BMR/TDEE", command=self.calculate)
        calculate_btn.grid(row=2, column=0, columnspan=2, pady=20)
        
        # 结果显示
        self.result_text = tk.Text(main_frame, height=12, width=50, state=tk.DISABLED)
        self.result_text.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # 状态栏
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
    
    def calculate(self):
        try:
            weight = float(self.weight_var.get())
            height = float(self.height_var.get())
            age = float(self.age_var.get())
            gender = self.gender_var.get()
            activity = self.activity_var.get()
            
            # 计算 BMR
            if gender == "男":
                bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
            else:
                bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
            
            # 活动系数
            activity_multipliers = {
                '久坐': 1.2,
                '轻度活动': 1.375,
                '中度活动': 1.55,
                '重度活动': 1.725,
                '极重度活动': 1.9
            }
            
            tdee = bmr * activity_multipliers.get(activity, 1.55)
            
            # 显示结果
            result = f"""【计算结果】

基础代谢率 (BMR): {bmr:.0f} 千卡/天
每日总消耗 (TDEE): {tdee:.0f} 千卡/天

【热量建议】
• 减肥: {tdee * 0.8:.0f} 千卡/天
• 维持: {tdee:.0f} 千卡/天  
• 增肌: {tdee * 1.1:.0f} 千卡/天

【活动水平说明】
• 久坐: 办公室工作，很少运动
• 轻度: 每周1-3天轻度运动
• 中度: 每周3-5天中度运动
• 重度: 每周6-7天高强度运动
• 极重度: 体力劳动者/运动员"""
            
            self.result_text.config(state=tk.NORMAL)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, result)
            self.result_text.config(state=tk.DISABLED)
            
            self.status_var.set("计算完成")
            
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
            self.status_var.set("输入错误")
        except Exception as e:
            messagebox.showerror("错误", f"计算时出现错误: {str(e)}")
            self.status_var.set("计算错误")

def main():
    root = tk.Tk()
    app = BMRCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()