#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""video-script-creator engine - 短视频脚本生成器"""

from __future__ import print_function
import sys
import random
import argparse
import textwrap

# ============================================================
# 平台配置
# ============================================================

PLATFORMS = {
    "douyin": {
        "name": "抖音",
        "style": "快节奏、强钩子、口语化、情绪拉满",
        "tags_prefix": "#抖音",
        "audience": "18-35岁，碎片化浏览",
        "tips": [
            "前3秒必须抓住注意力",
            "多用反问/悬念开场",
            "节奏紧凑，每5-8秒一个信息点",
            "结尾引导点赞+关注",
            "背景音乐很重要，选热门BGM",
        ],
    },
    "kuaishou": {
        "name": "快手",
        "style": "接地气、真实感、故事性强",
        "tags_prefix": "#快手",
        "audience": "下沉市场为主，注重真实和共鸣",
        "tips": [
            "真实感第一，不要太做作",
            "讲故事比讲道理更有效",
            "多展示过程和细节",
            "老铁文化，互动感强",
            "家庭/生活/手艺类内容受欢迎",
        ],
    },
    "youtube": {
        "name": "YouTube Shorts",
        "style": "信息密度高、国际化视角、字幕清晰",
        "tags_prefix": "#Shorts",
        "audience": "全球用户，偏好高质量内容",
        "tips": [
            "开场直奔主题，不要铺垫",
            "信息密度要高",
            "画面质量要求较高",
            "可中英双语字幕",
            "结尾引导订阅",
        ],
    },
    "bilibili": {
        "name": "B站",
        "style": "有深度、有梗、知识型/二次元友好",
        "tags_prefix": "#bilibili",
        "audience": "Z世代，喜欢有深度有趣的内容",
        "tips": [
            "可以稍微深入一点，观众有耐心",
            "玩梗要自然，不要硬蹭",
            "知识科普类很受欢迎",
            "弹幕互动文化，留互动点",
            "一键三连引导要自然",
        ],
    },
}

DURATIONS = {
    30: {"label": "30秒", "sections": 3, "words": "80-120字"},
    60: {"label": "60秒", "sections": 5, "words": "180-250字"},
    90: {"label": "90秒", "sections": 7, "words": "280-380字"},
}

# ============================================================
# 模板数据
# ============================================================

HOOK_TEMPLATES = [
    "【反问型】{topic}？90%的人都做错了！",
    "【悬念型】关于{topic}，我发现了一个惊人的秘密……",
    "【数字型】{topic}的3个隐藏技巧，第2个太绝了！",
    "【痛点型】还在为{topic}发愁？看完这条视频你就懂了",
    "【对比型】{topic}：新手 vs 高手的区别，差距太大了！",
    "【故事型】我花了3年才明白{topic}的真相……",
    "【挑战型】{topic}挑战！你敢试试吗？",
    "【揭秘型】{topic}的行业内幕，从来没人告诉你！",
    "【共鸣型】如果你也在纠结{topic}，一定要看完！",
    "【反常识型】{topic}？你以为的常识其实都是错的！",
]

TITLE_TEMPLATES = [
    "🔥 {topic}｜99%的人不知道的{n}个秘密",
    "💡 一分钟学会{topic}，小白也能秒懂！",
    "⚡ {topic}避坑指南！别再踩雷了",
    "🎯 {topic}终极攻略，看这一条就够了",
    "😱 {topic}的真相，看完我沉默了……",
    "✨ 手把手教你{topic}，从零到精通",
    "🚀 {topic}效率翻倍的{n}个神技巧",
    "💰 {topic}省钱秘籍，一年能省好几千",
    "❌ {topic}千万别这样做！我踩过的坑",
    "🏆 {topic}天花板教程，学到就是赚到",
]

CTA_TEMPLATES = [
    "觉得有用的话，双击屏幕给个❤️，关注我学习更多{topic}干货！",
    "你在{topic}方面有什么经验？评论区告诉我，我会一一回复！",
    "转发给你身边需要的人，收藏起来以后用得到！关注 @账号名 不迷路～",
    "{topic}系列持续更新中！点击关注，下期教你更进阶的玩法🔥",
    "如果这条视频帮到你了，点个赞让更多人看到！还想看什么主题？评论区留言📝",
    "这只是{topic}的冰山一角！关注我，带你解锁更多隐藏技能✨",
    "学会了吗？学会的扣1，没学会的扣2，我出详细教程！",
    "赶紧收藏！下次需要{topic}的时候就不用到处找了📌",
]

OUTLINE_SECTIONS = [
    {"name": "开场钩子", "desc": "3秒内抓住注意力，抛出核心悬念或痛点", "duration_pct": 10},
    {"name": "问题/痛点", "desc": "明确观众的困扰，引发共鸣", "duration_pct": 15},
    {"name": "核心内容", "desc": "干货输出，分2-3个要点展开", "duration_pct": 45},
    {"name": "案例/演示", "desc": "用实例或演示强化说服力", "duration_pct": 15},
    {"name": "总结+CTA", "desc": "回扣主题，引导互动（点赞/关注/评论）", "duration_pct": 15},
]

TRENDING_CATEGORIES = [
    {
        "category": "🎓 知识科普",
        "examples": ["冷知识合集", "一分钟看懂XX", "XX的前世今生"],
        "heat": "🔥🔥🔥🔥🔥",
    },
    {
        "category": "💼 职场成长",
        "examples": ["面试技巧", "副业赚钱", "职场避坑"],
        "heat": "🔥🔥🔥🔥",
    },
    {
        "category": "🍳 美食教程",
        "examples": ["快手菜", "一人食", "复刻网红美食"],
        "heat": "🔥🔥🔥🔥🔥",
    },
    {
        "category": "💪 健身运动",
        "examples": ["居家健身", "体态矫正", "减脂餐"],
        "heat": "🔥🔥🔥🔥",
    },
    {
        "category": "🛍️ 好物推荐",
        "examples": ["平价替代", "年度爱用", "避雷清单"],
        "heat": "🔥🔥🔥🔥🔥",
    },
    {
        "category": "🏠 生活技巧",
        "examples": ["收纳整理", "清洁妙招", "租房攻略"],
        "heat": "🔥🔥🔥🔥",
    },
    {
        "category": "💻 科技数码",
        "examples": ["APP推荐", "手机技巧", "AI工具"],
        "heat": "🔥🔥🔥🔥🔥",
    },
    {
        "category": "🎭 剧情/反转",
        "examples": ["职场小剧场", "情侣日常", "反转神结局"],
        "heat": "🔥🔥🔥",
    },
    {
        "category": "✈️ 旅行探店",
        "examples": ["小众景点", "城市citywalk", "探店打卡"],
        "heat": "🔥🔥🔥🔥",
    },
    {
        "category": "📚 读书分享",
        "examples": ["3分钟读完一本书", "书单推荐", "读书笔记"],
        "heat": "🔥🔥🔥",
    },
]

STORYBOARD_CUES = [
    "【镜头】正脸中景，直视镜头，表情{emotion}",
    "【镜头】产品/素材特写，手指指向重点",
    "【镜头】画面切换，插入相关素材/图片",
    "【镜头】全景展示环境/场景",
    "【镜头】屏幕录制/操作演示",
    "【镜头】文字弹出动效，强调关键信息",
    "【镜头】对比画面，左右分屏",
    "【镜头】慢动作/快进，增加节奏感",
]

EMOTIONS = ["认真", "惊讶", "兴奋", "严肃", "微笑", "夸张", "思考"]


# ============================================================
# 核心函数
# ============================================================

def print_divider(char="─", length=50):
    print(char * length)


def print_header(title):
    print("")
    print_divider("═")
    print("  {}".format(title))
    print_divider("═")
    print("")


def gen_script(topic, platform="douyin", duration=60):
    """生成完整短视频脚本"""
    plat = PLATFORMS.get(platform, PLATFORMS["douyin"])
    dur = DURATIONS.get(duration, DURATIONS[60])

    print_header("📹 短视频脚本 — {}".format(plat["name"]))

    print("📌 主题：{}".format(topic))
    print("📱 平台：{}（{}）".format(plat["name"], plat["style"]))
    print("⏱️  时长：{}（口播约{}）".format(dur["label"], dur["words"]))
    print("")
    print_divider()

    # 平台Tips
    print("")
    print("💡 平台要点：")
    for tip in plat["tips"]:
        print("   • {}".format(tip))
    print("")
    print_divider()

    # 开场（前3秒）
    print("")
    print("🎬 【第一幕 · 开场钩子】（0-3秒）")
    print("")
    hook = random.choice(HOOK_TEMPLATES).format(topic=topic)
    emotion = random.choice(EMOTIONS)
    cue = random.choice(STORYBOARD_CUES).format(emotion=emotion)
    print("   口播：「{}」".format(hook))
    print("   {}".format(cue))
    print("   🎵 BGM：节奏感强的热门音乐，从第一秒开始")
    print("")
    print_divider("·")

    # 主体
    section_count = dur["sections"] - 2  # 去掉开场和结尾
    if section_count < 1:
        section_count = 1

    time_per_section = (duration - 10) // section_count  # 留10秒给开场和结尾

    for i in range(section_count):
        start = 3 + i * time_per_section
        end = start + time_per_section
        print("")
        print("📝 【第{}幕 · 核心内容{}】（{}-{}秒）".format(
            i + 2,
            "·要点{}".format(i + 1) if section_count > 1 else "",
            start, end
        ))
        print("")

        prompts = [
            "围绕「{}」展开第{}个要点".format(topic, i + 1),
            "用具体案例或数据支撑观点",
            "语言口语化，避免书面语",
        ]
        if i == 0:
            prompts.append("承接开场钩子，自然过渡")
        if platform == "bilibili":
            prompts.append("可以适当玩梗，增加趣味性")
        if platform == "kuaishou":
            prompts.append("多用真实经历/故事来讲述")

        print("   口播要点：")
        for p in prompts:
            print("      → {}".format(p))

        emotion = random.choice(EMOTIONS)
        cue = random.choice(STORYBOARD_CUES).format(emotion=emotion)
        print("   {}".format(cue))
        print("   📌 字幕关键词：{}".format(topic))
        print("")
        print_divider("·")

    # 结尾
    print("")
    print("🎯 【最终幕 · 结尾CTA】（最后5秒）")
    print("")
    cta = random.choice(CTA_TEMPLATES).format(topic=topic)
    print("   口播：「{}」".format(cta))
    emotion = random.choice(EMOTIONS)
    cue = STORYBOARD_CUES[0].format(emotion=emotion)
    print("   {}".format(cue))
    print("   🎵 BGM渐弱，留出口播空间")
    print("")
    print_divider()

    # 标签推荐
    print("")
    print("🏷️  推荐标签：")
    base_tags = [
        "{} #{}".format(plat["tags_prefix"], topic),
        "#短视频",
        "#干货分享",
        "#涨知识",
        "#必看",
    ]
    for tag in base_tags:
        print("   {}".format(tag))

    print("")
    print_divider()
    print("")
    print("📋 脚本备注：")
    print("   • 以上为框架模板，请根据实际内容填充具体口播词")
    print("   • 建议先录音频确认节奏，再拍画面")
    print("   • {}平台建议竖屏拍摄（9:16）".format(plat["name"]))
    print("   • 字幕建议用醒目颜色+描边，放在画面下方1/3处")
    print("")


def gen_hooks(topic):
    """生成5个开场钩子"""
    print_header("🪝 开场钩子 · 前3秒留人")
    print("📌 主题：{}".format(topic))
    print("")
    print_divider()
    print("")

    selected = random.sample(HOOK_TEMPLATES, min(5, len(HOOK_TEMPLATES)))
    for i, tmpl in enumerate(selected, 1):
        hook = tmpl.format(topic=topic)
        print("{}. {}".format(i, hook))
        print("")

    print_divider()
    print("")
    print("💡 使用技巧：")
    print("   • 语速要快，语气要强，表情要到位")
    print("   • 前3秒决定完播率，反复测试不同钩子")
    print("   • 可以搭配画面闪切+音效增强冲击力")
    print("   • A/B测试：同一内容用不同钩子发布，看数据选最优")
    print("")


def gen_titles(topic):
    """生成5个爆款标题"""
    print_header("✍️  爆款标题生成器")
    print("📌 主题：{}".format(topic))
    print("")
    print_divider()
    print("")

    selected = random.sample(TITLE_TEMPLATES, min(5, len(TITLE_TEMPLATES)))
    for i, tmpl in enumerate(selected, 1):
        n = random.choice([3, 5, 7, 10])
        title = tmpl.format(topic=topic, n=n)
        print("{}. {}".format(i, title))
        print("")

    print_divider()
    print("")
    print("💡 标题优化技巧：")
    print("   • 数字+情绪词=高点击率")
    print("   • 控制在20字以内，手机端完整展示")
    print("   • 善用emoji增加视觉吸引力")
    print("   • 制造信息差/好奇心缺口")
    print("   • 蹭热点但不要标题党")
    print("")


def gen_outline(topic):
    """生成视频大纲"""
    print_header("📋 视频大纲")
    print("📌 主题：{}".format(topic))
    print("")
    print_divider()
    print("")

    for i, section in enumerate(OUTLINE_SECTIONS, 1):
        bar_len = section["duration_pct"] // 5
        bar = "█" * bar_len + "░" * (10 - bar_len)
        print("{} {} [{}] (占比 {}%)".format(
            i, section["name"], bar, section["duration_pct"]
        ))
        print("   {}".format(section["desc"]))
        print("")

    print_divider()
    print("")
    print("📐 大纲应用建议：")
    print("")
    print("   30秒视频：压缩为 钩子→核心1点→CTA 三段式")
    print("   60秒视频：完整五段式，每段10-15秒")
    print("   90秒视频：核心内容可拆分2-3个子要点，加案例")
    print("")
    print("   通用公式：")
    print("   钩子（抓注意力）→ 痛点（引共鸣）→ 干货（给价值）")
    print("   → 案例（增信任）→ CTA（促行动）")
    print("")


def gen_cta(topic):
    """生成结尾CTA"""
    print_header("🎯 结尾互动引导（CTA）")
    print("📌 主题：{}".format(topic))
    print("")
    print_divider()
    print("")

    selected = random.sample(CTA_TEMPLATES, min(5, len(CTA_TEMPLATES)))
    for i, tmpl in enumerate(selected, 1):
        cta = tmpl.format(topic=topic)
        print("{}. {}".format(i, cta))
        print("")

    print_divider()
    print("")
    print("💡 CTA技巧：")
    print("   • 明确告诉观众要做什么（点赞/关注/评论/收藏）")
    print("   • 给一个互动理由，不要硬求")
    print("   • 提问式CTA效果最好（引发评论区讨论）")
    print("   • 预告下期内容，制造期待感")
    print("   • 语气真诚自然，不要太套路")
    print("")


def gen_trending():
    """展示热门视频类型"""
    print_header("🔥 热门短视频类型 & 方向")
    print("")

    for item in TRENDING_CATEGORIES:
        print("{} {}".format(item["category"], item["heat"]))
        examples_str = " / ".join(item["examples"])
        print("   热门选题：{}".format(examples_str))
        print("")

    print_divider()
    print("")
    print("💡 选题建议：")
    print("   • 从自己擅长的领域切入，真实感最重要")
    print("   • 关注各平台热搜/话题榜，借势不造势")
    print("   • 垂直领域深耕 > 什么都拍")
    print("   • 爆款公式：热门话题 × 个人特色 × 实用价值")
    print("   • 多看同类型头部账号，学习选题角度")
    print("")


def show_help():
    """显示帮助信息"""
    print_header("📹 video-script-creator · 短视频脚本生成器")

    print("支持平台：抖音 | 快手 | YouTube Shorts | B站")
    print("")
    print_divider()
    print("")
    print("📖 命令列表：")
    print("")

    commands = [
        ("script \"主题\"", "生成完整脚本（开场-主体-结尾+分镜提示）"),
        ("", "  选项: --platform douyin|kuaishou|youtube|bilibili"),
        ("", "         --duration 30|60|90"),
        ("hook \"主题\"", "生成5个开场钩子（前3秒留人）"),
        ("title \"主题\"", "生成5个爆款标题"),
        ("outline \"主题\"", "生成视频大纲"),
        ("cta \"主题\"", "生成结尾引导互动文案"),
        ("trending", "热门视频类型/方向"),
        ("help", "显示此帮助信息"),
    ]

    for cmd, desc in commands:
        if cmd:
            print("  {:<30s} {}".format(cmd, desc))
        else:
            print("  {:<30s} {}".format("", desc))

    print("")
    print_divider()
    print("")
    print("📝 示例：")
    print("")
    print("  video-script.sh script \"咖啡拉花教程\" --platform douyin --duration 60")
    print("  video-script.sh hook \"租房避坑\"")
    print("  video-script.sh title \"Python入门\"")
    print("  video-script.sh trending")
    print("")


# ============================================================
# 主入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1]

    if command == "help":
        show_help()
        return

    if command == "trending":
        gen_trending()
        return

    # 以下命令需要主题参数
    if command in ("script", "hook", "title", "outline", "cta"):
        # 解析参数
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument("command")
        parser.add_argument("topic", nargs="?", default=None)
        parser.add_argument("--platform", default="douyin",
                            choices=["douyin", "kuaishou", "youtube", "bilibili"])
        parser.add_argument("--duration", type=int, default=60,
                            choices=[30, 60, 90])

        args = parser.parse_args()

        if not args.topic:
            print("❌ 请提供主题！")
            print("用法：video-script.sh {} \"你的主题\"".format(command))
            sys.exit(1)

        topic = args.topic

        if command == "script":
            gen_script(topic, args.platform, args.duration)
        elif command == "hook":
            gen_hooks(topic)
        elif command == "title":
            gen_titles(topic)
        elif command == "outline":
            gen_outline(topic)
        elif command == "cta":
            gen_cta(topic)
    else:
        print("❌ 未知命令: {}".format(command))
        print("运行 'video-script.sh help' 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()
