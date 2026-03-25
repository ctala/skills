"""Order 下单技能模块 - 完整的下单流程"""

import typer
import asyncio
import json
import re
from typing import Optional, List
from .api_client import api_client

order_app = typer.Typer(name="order", help="下单订货流程技能")


def sync_run(coroutine):
    """同步运行异步函数"""
    return asyncio.get_event_loop().run_until_complete(coroutine)


def handle_errors(func):
    """错误处理装饰器，提供结构化的错误输出"""
    import functools
    import traceback
    import json as json_module
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 从参数中获取json_output，如果不存在则默认为False
        json_output = kwargs.get('json_output', False)
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if json_output:
                error_data = {
                    "error": True,
                    "type": type(e).__name__,
                    "message": str(e),
                    "traceback": traceback.format_exc() if hasattr(e, '__traceback__') else None
                }
                typer.echo(json_module.dumps(error_data, ensure_ascii=False, indent=2))
                # 输出JSON错误后退出，退出码为1
                raise typer.Exit(code=1)
            else:
                # 让Typer处理默认错误输出
                raise
    
    return wrapper


@order_app.command("place")
@handle_errors
def place_order(
    dealer_code: str = typer.Option(..., "-dealer", "--dealer-code", help="客户编号"),
    dealer_name: str = typer.Option(..., "-name", "--dealer-name", help="客户名称"),
    sales_code: str = typer.Option(..., "-sales", "--sales-code", help="业务员编号"),
    product_codes: str = typer.Option(..., "-products", "--product-codes", help="商品编号列表，逗号分隔"),
    departure_base: str = typer.Option(..., "-base", "--departure-base", help="发货基地"),
    destination: str = typer.Option(..., "-dest", "--destination", help="收货地址"),
    transport_mode: str = typer.Option("汽运", "-transport", "--transport-mode", help="运输方式，默认汽运"),
    pickup_mode: str = typer.Option("统派车（客户付款）", "-pickup", "--pickup-mode", help="提货方式，默认统派车（客户付款）"),
    receiver_name: str = typer.Option("", "-receiver", "--receiver-name", help="收货人姓名"),
    receiver_phone: str = typer.Option("", "-phone", "--receiver-phone", help="收货人电话"),
    cover_image_urls: Optional[str] = typer.Option(None, "-images", "--cover-images", help="商品封面图 URL 列表，逗号分隔"),
    quantities: Optional[str] = typer.Option(None, "-q", "--quantities", help="商品数量列表，逗号分隔，与商品编号一一对应，默认为1"),
    json_output: bool = typer.Option(False, "-j", "--json", help="输出JSON格式")
):
    """
    完成下单流程，生成订单页面 URL

    示例：
    order place -dealer "J620522007" -name "牛建建" -sales "EZB2019063" \\
                -products "Y163U1305276020000" -base "新洋丰中磷" \\
                -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
    
    带数量的示例：
    order place -dealer "J620522007" -name "牛建建" -sales "EZB2019063" \\
                -products "Y163U1305276020000,ABC123456789" \\
                -q "5,3" -base "新洋丰中磷" \\
                -dest "湖北省荆门市东宝区泉口街道馨梦缘公寓"
    """
    # 解析商品编号列表
    product_code_list = [p.strip() for p in product_codes.split(",") if p.strip()]

    # 解析封面图 URL 列表
    image_url_list = []
    if cover_image_urls:
        image_url_list = [url.strip() for url in cover_image_urls.split(",") if url.strip()]

    # 解析数量列表
    quantity_list = []
    if quantities:
        try:
            quantity_list = [int(q.strip()) for q in quantities.split(",") if q.strip()]
            if len(quantity_list) != len(product_code_list):
                raise typer.BadParameter(
                    f"数量列表长度({len(quantity_list)})与商品编号列表长度({len(product_code_list)})不匹配"
                )
            # 验证数量是否为正整数
            for q in quantity_list:
                if q <= 0:
                    raise typer.BadParameter(f"商品数量必须为正整数，当前值: {q}")
        except ValueError:
            raise typer.BadParameter("数量列表必须为逗号分隔的整数")
    else:
        # 默认所有商品数量为1
        quantity_list = [1] * len(product_code_list)

    # 构建商品列表
    product_list = []
    for i, code in enumerate(product_code_list):
        product_info = {
            "product_code": code,
            "cover_image_url": image_url_list[i] if i < len(image_url_list) else "",
            "quantity": quantity_list[i]
        }
        product_list.append(product_info)

    # 构建请求数据
    order_data = {
        "customer_code": dealer_code,
        "customer_name": dealer_name,
        "sales_code": sales_code,
        "product_list": product_list,
        "departure_base": departure_base,
        "destination": destination,
        "transport_mode": transport_mode,
        "pickup_mode": pickup_mode,
        "receiver_name": receiver_name,
        "receiver_phone": receiver_phone
    }

    async def _run():
        result = await api_client.post("/getorderaddress", order_data)
        return result

    result = sync_run(_run())

    # 输出结果
    if json_output:
        output_data = {
            "order_data": order_data,
            "api_response": result
        }
        typer.echo(json.dumps(output_data, ensure_ascii=False, indent=2))
    else:
        typer.echo("=" * 50)
        typer.echo("订单信息页面 URL 生成成功")
        typer.echo("=" * 50)

        if isinstance(result, dict):
            if "url" in result:
                typer.echo(f"\n订单页面 URL: {result['url']}")

            if "message" in result:
                typer.echo(f"消息：{result['message']}")

            if "order_info" in result:
                typer.echo("\n订单详情:")
                order_info = result["order_info"]
                typer.echo(f"  客户编号：{order_info.get('customer_code', '')}")
                typer.echo(f"  客户名称：{order_info.get('customer_name', '')}")
                typer.echo(f"  业务员编号：{order_info.get('sales_code', '')}")
                typer.echo(f"  发货基地：{order_info.get('departure_base', '')}")
                typer.echo(f"  运输方式：{order_info.get('transport_mode', '')}")
                typer.echo(f"  提货方式：{order_info.get('pickup_mode', '')}")
                typer.echo(f"  收货地址：{order_info.get('destination', '')}")
                typer.echo(f"  收货人：{order_info.get('receiver_name', '')}")
                typer.echo(f"  收货人电话：{order_info.get('receiver_phone', '')}")
                typer.echo("  商品列表:")
                for product in order_info.get("product_list", []):
                    product_code = product.get('product_code', '')
                    quantity = product.get('quantity', 1)
                    if quantity != 1:
                        typer.echo(f"    - {product_code} ×{quantity}")
                    else:
                        typer.echo(f"    - {product_code}")
        else:
            typer.echo(result)

