#!/usr/bin/env python3
"""
💼 08_enterprise/microservices_logging.py
微服務日誌架構範例

這個範例展示了如何在微服務架構中實現統一的日誌管理，
包含分散式追蹤、服務間日誌關聯、統一格式標準和日誌聚合策略。
"""

import uuid
import asyncio
import json
from typing import Dict, Optional, Any
from contextvars import ContextVar
from datetime import datetime
from pretty_loguru import create_logger

# 全域追蹤上下文
trace_id_var: ContextVar[Optional[str]] = ContextVar('trace_id', default=None)
span_id_var: ContextVar[Optional[str]] = ContextVar('span_id', default=None)
service_name_var: ContextVar[Optional[str]] = ContextVar('service_name', default=None)

class DistributedTracing:
    """分散式追蹤管理器"""
    
    def __init__(self):
        self.traces: Dict[str, Dict] = {}
    
    def start_trace(self, service_name: str) -> str:
        """開始新的追蹤"""
        trace_id = str(uuid.uuid4())
        trace_id_var.set(trace_id)
        service_name_var.set(service_name)
        
        self.traces[trace_id] = {
            'trace_id': trace_id,
            'service_name': service_name,
            'start_time': datetime.utcnow().isoformat(),
            'spans': []
        }
        
        return trace_id
    
    def start_span(self, operation: str, parent_span_id: str = None) -> str:
        """開始新的 span"""
        span_id = str(uuid.uuid4())
        span_id_var.set(span_id)
        
        span_data = {
            'span_id': span_id,
            'parent_span_id': parent_span_id,
            'operation': operation,
            'start_time': datetime.utcnow().isoformat(),
            'service_name': service_name_var.get()
        }
        
        trace_id = trace_id_var.get()
        if trace_id and trace_id in self.traces:
            self.traces[trace_id]['spans'].append(span_data)
        
        return span_id
    
    def end_span(self, span_id: str, status: str = "success", metadata: Dict = None):
        """結束 span"""
        trace_id = trace_id_var.get()
        if trace_id and trace_id in self.traces:
            for span in self.traces[trace_id]['spans']:
                if span['span_id'] == span_id:
                    span['end_time'] = datetime.utcnow().isoformat()
                    span['status'] = status
                    span['metadata'] = metadata or {}
                    break
    
    def get_trace_context(self) -> Dict[str, Any]:
        """獲取當前追蹤上下文"""
        return {
            'trace_id': trace_id_var.get(),
            'span_id': span_id_var.get(),
            'service_name': service_name_var.get()
        }

class MicroserviceLogger:
    """微服務專用日誌記錄器"""
    
    def __init__(self, service_name: str, log_dir: str = "logs/microservices"):
        self.service_name = service_name
        self.tracer = DistributedTracing()
        
        # 建立服務專用的日誌記錄器
        self.logger = create_logger(
            name=f"microservice_{service_name}",
            log_dir=f"{log_dir}/{service_name}",
            level="INFO",
            rotation="daily",
            retention="30 days"
        )
        
        # 啟動服務日誌
        self.logger.info(
            f"🚀 微服務 {service_name} 啟動",
            extra={
                'service_name': service_name,
                'event_type': 'service_start',
                'timestamp': datetime.utcnow().isoformat()
            }
        )
    
    def log_request(self, method: str, path: str, user_id: str = None, 
                    request_data: Dict = None, response_data: Dict = None):
        """記錄請求日誌"""
        context = self.tracer.get_trace_context()
        
        log_data = {
            'event_type': 'request',
            'method': method,
            'path': path,
            'user_id': user_id,
            'request_data': request_data or {},
            'response_data': response_data or {},
            'timestamp': datetime.utcnow().isoformat(),
            **context
        }
        
        self.logger.info(f"📡 {method} {path}", extra=log_data)
    
    def log_database_operation(self, operation: str, table: str, 
                              query_time: float, affected_rows: int = None):
        """記錄資料庫操作日誌"""
        context = self.tracer.get_trace_context()
        
        log_data = {
            'event_type': 'database_operation',
            'operation': operation,
            'table': table,
            'query_time_ms': round(query_time * 1000, 2),
            'affected_rows': affected_rows,
            'timestamp': datetime.utcnow().isoformat(),
            **context
        }
        
        self.logger.info(f"🗃️ DB {operation} on {table}", extra=log_data)
    
    def log_service_call(self, target_service: str, endpoint: str, 
                        response_time: float, status_code: int):
        """記錄服務間呼叫日誌"""
        context = self.tracer.get_trace_context()
        
        log_data = {
            'event_type': 'service_call',
            'target_service': target_service,
            'endpoint': endpoint,
            'response_time_ms': round(response_time * 1000, 2),
            'status_code': status_code,
            'timestamp': datetime.utcnow().isoformat(),
            **context
        }
        
        status = "success" if 200 <= status_code < 300 else "error"
        self.logger.info(f"🔗 Call to {target_service}{endpoint} ({status})", extra=log_data)
    
    def log_business_event(self, event_name: str, event_data: Dict = None):
        """記錄業務事件日誌"""
        context = self.tracer.get_trace_context()
        
        log_data = {
            'event_type': 'business_event',
            'event_name': event_name,
            'event_data': event_data or {},
            'timestamp': datetime.utcnow().isoformat(),
            **context
        }
        
        self.logger.info(f"💼 {event_name}", extra=log_data)

async def simulate_user_service():
    """模擬用戶服務"""
    logger = MicroserviceLogger("user_service")
    
    # 開始追蹤
    trace_id = logger.tracer.start_trace("user_service")
    
    # 模擬用戶註冊流程
    span_id = logger.tracer.start_span("user_registration")
    
    try:
        # 記錄 API 請求
        logger.log_request(
            method="POST",
            path="/api/users/register",
            user_id="new_user_123",
            request_data={'email': 'user@example.com', 'username': 'newuser'}
        )
        
        # 模擬資料庫操作
        await asyncio.sleep(0.1)  # 模擬 DB 延遲
        logger.log_database_operation(
            operation="INSERT",
            table="users",
            query_time=0.1,
            affected_rows=1
        )
        
        # 模擬呼叫郵件服務
        await asyncio.sleep(0.05)  # 模擬網路延遲
        logger.log_service_call(
            target_service="email_service",
            endpoint="/send-welcome-email",
            response_time=0.05,
            status_code=200
        )
        
        # 記錄業務事件
        logger.log_business_event(
            event_name="user_registered",
            event_data={
                'user_id': 'new_user_123',
                'registration_source': 'web',
                'plan': 'free'
            }
        )
        
        logger.tracer.end_span(span_id, "success")
        
    except Exception as e:
        logger.tracer.end_span(span_id, "error", {'error': str(e)})
        logger.logger.error(f"用戶註冊失敗: {e}")

async def simulate_order_service():
    """模擬訂單服務"""
    logger = MicroserviceLogger("order_service")
    
    # 開始追蹤
    trace_id = logger.tracer.start_trace("order_service")
    
    # 模擬訂單處理流程
    span_id = logger.tracer.start_span("order_processing")
    
    try:
        # 記錄 API 請求
        logger.log_request(
            method="POST",
            path="/api/orders",
            user_id="user_456",
            request_data={'items': [{'id': 'item_1', 'quantity': 2}], 'total': 99.99}
        )
        
        # 模擬庫存檢查服務呼叫
        await asyncio.sleep(0.08)
        logger.log_service_call(
            target_service="inventory_service",
            endpoint="/check-stock",
            response_time=0.08,
            status_code=200
        )
        
        # 模擬支付服務呼叫
        await asyncio.sleep(0.12)
        logger.log_service_call(
            target_service="payment_service",
            endpoint="/process-payment",
            response_time=0.12,
            status_code=200
        )
        
        # 模擬訂單資料庫操作
        await asyncio.sleep(0.06)
        logger.log_database_operation(
            operation="INSERT",
            table="orders",
            query_time=0.06,
            affected_rows=1
        )
        
        # 記錄業務事件
        logger.log_business_event(
            event_name="order_created",
            event_data={
                'order_id': 'order_789',
                'user_id': 'user_456',
                'amount': 99.99,
                'payment_method': 'credit_card'
            }
        )
        
        logger.tracer.end_span(span_id, "success")
        
    except Exception as e:
        logger.tracer.end_span(span_id, "error", {'error': str(e)})
        logger.logger.error(f"訂單處理失敗: {e}")

async def simulate_notification_service():
    """模擬通知服務"""
    logger = MicroserviceLogger("notification_service")
    
    # 開始追蹤
    trace_id = logger.tracer.start_trace("notification_service")
    
    # 模擬通知發送流程
    span_id = logger.tracer.start_span("notification_sending")
    
    try:
        # 記錄 API 請求
        logger.log_request(
            method="POST",
            path="/api/notifications/send",
            user_id="user_456",
            request_data={'type': 'order_confirmation', 'channels': ['email', 'sms']}
        )
        
        # 模擬郵件發送
        await asyncio.sleep(0.03)
        logger.log_service_call(
            target_service="email_service",
            endpoint="/send-email",
            response_time=0.03,
            status_code=200
        )
        
        # 模擬簡訊發送
        await asyncio.sleep(0.02)
        logger.log_service_call(
            target_service="sms_service",
            endpoint="/send-sms",
            response_time=0.02,
            status_code=200
        )
        
        # 記錄業務事件
        logger.log_business_event(
            event_name="notification_sent",
            event_data={
                'user_id': 'user_456',
                'notification_type': 'order_confirmation',
                'channels': ['email', 'sms']
            }
        )
        
        logger.tracer.end_span(span_id, "success")
        
    except Exception as e:
        logger.tracer.end_span(span_id, "error", {'error': str(e)})
        logger.logger.error(f"通知發送失敗: {e}")

async def main():
    """主函數 - 模擬微服務架構"""
    print("🏗️ 微服務日誌架構演示")
    print("=" * 50)
    
    # 建立服務聚合日誌記錄器
    aggregator_logger = create_logger(
        name="microservices_aggregator",
        log_dir="logs/aggregator",
        level="INFO",
        rotation="daily"
    )
    
    aggregator_logger.info("🚀 微服務集群啟動")
    
    # 並行運行多個微服務
    tasks = [
        simulate_user_service(),
        simulate_order_service(),
        simulate_notification_service()
    ]
    
    await asyncio.gather(*tasks)
    
    aggregator_logger.info("✅ 微服務集群運行完成")
    
    print("\n📊 微服務日誌架構演示完成！")
    print("📁 日誌檔案位置:")
    print("   - logs/microservices/user_service/")
    print("   - logs/microservices/order_service/")
    print("   - logs/microservices/notification_service/")
    print("   - logs/aggregator/")

if __name__ == "__main__":
    asyncio.run(main())