

# 添加宫位名称映射
PALACE_NAME_MAPPING = {
    "命宫": "命宫",
    "兄弟": "兄弟宫",
    "夫妻": "夫妻宫",
    "子女": "子女宫",
    "财帛": "财帛宫",
    "疾厄": "疾厄宫",
    "迁移": "迁移宫",
    "奴仆": "奴仆宫",
    "官禄": "官禄宫",
    "田宅": "田宅宫",
    "福德": "福德宫",
    "父母": "父母宫"
}

# 添加对宫关系字典
OPPOSITE_PALACE = {
    "命宫": "迁移宫",
    "兄弟宫": "奴仆宫",
    "夫妻宫": "官禄宫",
    "子女宫": "田宅宫",
    "财帛宫": "福德宫",
    "疾厄宫": "父母宫",
    "迁移宫": "命宫",
    "奴仆宫": "兄弟宫",
    "官禄宫": "夫妻宫",
    "田宅宫": "子女宫", 
    "福德宫": "财帛宫",
    "父母宫": "疾厄宫"
}

def convert_palace_json_to_text(json_data):
    """
    将单个宫位的紫微斗数 JSON 数据转换为文本描述。

    参数:
    json_data (dict): 包含单个宫位紫微斗数信息的 JSON 数据。

    返回:
    str: 描述单个宫位紫微斗数信息的文本字符串。
    """

    palace_name = json_data['name']
    full_palace_name = PALACE_NAME_MAPPING.get(palace_name, f"{palace_name}宫")
    
    # 构建更紧凑的宫位信息
    palace_text = f"{full_palace_name}"
    if json_data['isBodyPalace'] or json_data['isOriginalPalace']:
        palace_info = []
        if json_data['isBodyPalace']:
            palace_info.append("身宫")
        if json_data['isOriginalPalace']:
            palace_info.append("来因宫")
        palace_text += f"({', '.join(palace_info)})"
    
    palace_text += f" • {json_data['heavenlyStem']}{json_data['earthlyBranch']}"
    
    # 处理主星信息
    major_stars = json_data['majorStars']
    if major_stars:
        star_info = []
        for star in major_stars:
            brightness = star['brightness'] or ""
            mutagen = star.get('mutagen', "")
            
            # 精简星曜描述
            if star['type'] == 'tianma':
                star_info.append(f"{star['name']}")
            elif star['scope'] == 'origin':
                star_desc = f"{star['name']}"
                if brightness:
                    star_desc += f"({brightness})"
                if mutagen and star['type'] == 'major':
                    star_desc += f"(化{mutagen})"
                star_info.append(star_desc)
            else:
                star_desc = f"{star['name']}"
                if brightness:
                    star_desc += f"({brightness})"
                if mutagen:
                    star_desc += f"(化{mutagen})"
                star_info.append(star_desc)
        
        if star_info:
            palace_text += f"\n主星: {', '.join(star_info)}"
    else:
        # 空宫处理
        base_palace = f"{palace_name}宫"
        opposite = OPPOSITE_PALACE.get(base_palace, "未知宫位")
        if palace_name == '命宫':
            opposite = '迁移宫'
        palace_text += f"\n空宫(借{opposite}主星)"
    
    # 处理辅星信息
    minor_stars = json_data['minorStars']
    if minor_stars:
        minor_star_info = []
        for star in minor_stars:
            star_desc = star['name']
            # 添加亮度信息（如果有）
            brightness = star.get('brightness', '')
            if brightness:
                star_desc += f"({brightness})"
            minor_star_info.append(star_desc)
        palace_text += f"\n辅星: {', '.join(minor_star_info)}"
    
    # 处理杂耀信息
    adjective_stars = json_data['adjectiveStars']
    if adjective_stars:
        adj_names = [star['name'] for star in adjective_stars]
        palace_text += f"\n杂耀: {', '.join(adj_names)}"
    
    # 添加大限信息(如果有)
    decadal = json_data.get('decadal', {})
    if decadal:
        age_range = decadal.get('range', [])
        if len(age_range) == 2:
            palace_text += f"\n大限: {age_range[0]}-{age_range[1]}"
    
    return palace_text

def convert_main_json_to_text(main_json_data):
    """
    将包含个人信息和宫位数组的紫微斗数 JSON 数据转换为文本描述。

    参数:
    main_json_data (dict): 包含完整紫微斗数信息的 JSON 数据。

    返回:
    str: 描述完整紫微斗数信息的文本字符串。
    """
    output_lines = []

    # 基本信息更紧凑的格式
    output_lines.append("---基本信息---")
    gender = main_json_data.get('gender', '未知')
    chinese_date = main_json_data.get('chineseDate', '未知')
    
    # 确定天干的阴阳
    heavenly_stem_yin_yang = ""
    if chinese_date and len(chinese_date) >= 1:
        first_char = chinese_date[0]
        if first_char in ["甲", "丙", "戊", "庚", "壬"]:
            heavenly_stem_yin_yang = "阳"
        elif first_char in ["乙", "丁", "己", "辛", "癸"]:
            heavenly_stem_yin_yang = "阴"
    
    # 确定大运方向
    da_yun_direction = ""  # 暂时注释掉
    # if heavenly_stem_yin_yang == "阳" and gender == "男":
    #     da_yun_direction = "顺行（顺时针）"
    # elif heavenly_stem_yin_yang == "阳" and gender == "女":
    #     da_yun_direction = "逆行（逆时针）"
    # elif heavenly_stem_yin_yang == "阴" and gender == "男":
    #     da_yun_direction = "逆行（逆时针）"
    # elif heavenly_stem_yin_yang == "阴" and gender == "女":
    #     da_yun_direction = "顺行（顺时针）"
    
    # 更紧凑的基本信息显示
    output_lines.append(f"命主: {gender}命·{main_json_data.get('zodiac', '未知')}·{main_json_data.get('sign', '未知')}")
    output_lines.append(f"生日: 阳历{main_json_data.get('solarDate', '未知')}·阴历{main_json_data.get('lunarDate', '未知')}")
    output_lines.append(f"八字: {chinese_date}")
    output_lines.append(f"命盘: 命宫{main_json_data.get('earthlyBranchOfSoulPalace', '未知')}·身宫{main_json_data.get('earthlyBranchOfBodyPalace', '未知')}·{main_json_data.get('fiveElementsClass', '未知')}")
    output_lines.append(f"主星: 命主{main_json_data.get('soul', '未知')}·身主{main_json_data.get('body', '未知')}")
    # output_lines.append(f"大运: {da_yun_direction}")
        
    output_lines.append("---宫位信息---")

    # 宫位信息 (如果 palaces 数组存在且不为空)
    palaces_data = main_json_data.get('palaces')
    if palaces_data and isinstance(palaces_data, list):
        if not palaces_data:
            output_lines.append("宫位信息：暂未提供") # 或者其他提示信息
        else:
            # 按照大限年龄范围排序宫位
            sorted_palaces = sorted(palaces_data, key=lambda x: x.get('decadal', {}).get('range', [999, 999])[0])
            
            for palace_json in sorted_palaces:
                palace_text = convert_palace_json_to_text(palace_json)
                output_lines.append(palace_text)
                output_lines.append("---") # 分隔每个宫位的信息
    else:
        output_lines.append("宫位信息：数据格式不正确或缺失")

    return "\n".join(output_lines)

def convert_horoscope_to_text(horoscope_data, precision='yearly', target_date=None):
    """
    将运限数据转换为文本描述。

    参数:
    horoscope_data (dict): 包含运限信息的字典数据。
    precision (str): 运限时间精确性，可选值：
        - 'decadal': 只显示大限信息
        - 'yearly': 显示大限和流年信息
        - 'monthly': 显示大限、流年和流月信息
        - 'daily': 显示大限、流年、流月和流日信息
        - 'hourly': 显示所有运限信息
    target_date (str): 目标日期，格式为 "YYYY-MM-DD"，如果提供则只显示该日期的运限信息

    返回:
    str: 描述运限信息的文本字符串。
    """
    output_lines = []
    
    # 如果提供了目标日期，添加日期信息
    if target_date:
        output_lines.append(f"=== 运限日期: {target_date} ===")
    
    # 大限信息（始终显示）
    decadal = horoscope_data.get('decadal', {})
    if decadal:
        output_lines.append("\n=== 大限信息 ===")
        output_lines.append(f"大限: {decadal.get('heavenlyStem', '')}{decadal.get('earthlyBranch', '')}")
        output_lines.append(f"大限四化(化禄、化权、化科、化忌): {', '.join(decadal.get('mutagen', []))}")
    
    # 根据精确性级别显示不同信息
    if precision in ['yearly', 'monthly', 'daily', 'hourly']:
        # 流年信息
        yearly = horoscope_data.get('yearly', {})
        if yearly:
            output_lines.append("\n=== 流年信息 ===")
            output_lines.append(f"流年: {yearly.get('heavenlyStem', '')}{yearly.get('earthlyBranch', '')}")
            output_lines.append(f"流年四化(禄权科忌): {', '.join(yearly.get('mutagen', []))}")
            
            # 流年12神
            yearly_dec_star = yearly.get('yearlyDecStar', {})
            if yearly_dec_star:
                output_lines.append(f"将前12神: {', '.join(yearly_dec_star.get('jiangqian12', []))}")
                output_lines.append(f"岁前12神: {', '.join(yearly_dec_star.get('suiqian12', []))}")
    
    if precision in ['monthly', 'daily', 'hourly']:
        # 流月信息
        monthly = horoscope_data.get('monthly', {})
        if monthly:
            output_lines.append("\n=== 流月信息 ===")
            output_lines.append(f"流月: {monthly.get('heavenlyStem', '')}{monthly.get('earthlyBranch', '')}")
            output_lines.append(f"流月四化(禄权科忌): {', '.join(monthly.get('mutagen', []))}")
    
    if precision in ['daily', 'hourly']:
        # 流日信息
        daily = horoscope_data.get('daily', {})
        if daily:
            output_lines.append("\n=== 流日信息 ===")
            output_lines.append(f"流日: {daily.get('heavenlyStem', '')}{daily.get('earthlyBranch', '')}")
            output_lines.append(f"流日四化(禄权科忌): {', '.join(daily.get('mutagen', []))}")
    
    if precision == 'hourly':
        # 流时信息
        hourly = horoscope_data.get('hourly', {})
        if hourly:
            output_lines.append("\n=== 流时信息 ===")
            output_lines.append(f"流时: {hourly.get('heavenlyStem', '')}{hourly.get('earthlyBranch', '')}")
            output_lines.append(f"流时四化(禄权科忌): {', '.join(hourly.get('mutagen', []))}")
    
    return "\n".join(output_lines)