#!/usr/bin/env python3
"""
待办事项提醒脚本，用于定时检查即将到期的任务并发送通知
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from todo import check_due_tasks
import json

def send_reminder():
    """发送到期提醒"""
    due_tasks = check_due_tasks()
    
    if not due_tasks:
        return
    
    message = "⚠️  待办事项提醒\n"
    message += "=" * 30 + "\n"
    
    for task, reason in due_tasks:
        message += f"• [{task['id']}] {task['title']}\n"
        message += f"  {reason}\n"
        if task["description"]:
            message += f"  描述：{task['description']}\n"
        message += "\n"
    
    # 输出提醒信息，供cron调用时发送
    print(message)
    
    # 可选：通过feishu发送消息
    try:
        from feishu import send_message
        send_message(message)
    except ImportError:
        pass

if __name__ == "__main__":
    send_reminder()