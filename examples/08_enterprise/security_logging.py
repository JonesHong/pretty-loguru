#!/usr/bin/env python3
"""
🔒 08_enterprise/security_logging.py
安全相關日誌範例

這個範例展示了如何實現企業級的安全日誌記錄，
包含安全事件記錄、審計日誌要求、敏感資訊處理和入侵檢測日誌。
"""

import hashlib
import re
import json
from enum import Enum
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from pretty_loguru import create_logger

class SecurityEventType(Enum):
    """安全事件類型"""
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    LOGOUT = "logout"
    PASSWORD_CHANGE = "password_change"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    DATA_ACCESS = "data_access"
    DATA_EXPORT = "data_export"
    CONFIGURATION_CHANGE = "config_change"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"
    UNAUTHORIZED_ACCESS = "unauthorized_access"
    SECURITY_VIOLATION = "security_violation"
    AUDIT_EVENT = "audit_event"

class SecurityLevel(Enum):
    """安全級別"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class SecurityLogger:
    """安全事件專用日誌記錄器"""
    
    def __init__(self):
        self.failed_attempts: Dict[str, List[datetime]] = {}
        self.suspicious_ips: Set[str] = set()
        self.sensitive_patterns = [
            r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # 信用卡號
            r'\b\d{3}-\d{2}-\d{4}\b',  # SSN
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email
            r'\b(?:\d{1,3}\.){3}\d{1,3}\b',  # IP 地址
        ]
        
        # 建立安全日誌記錄器
        self.logger = create_logger(
            name="security_audit",
            log_dir="logs/security",
            level="INFO",
            preset="daily",
            retention="2555 days"  # 合規要求：安全日誌保留 7 years ≈ 2555 days
        )
        
        # 建立審計日誌記錄器
        self.audit_logger = create_logger(
            name="audit_trail",
            log_dir="logs/audit",
            level="INFO",
            preset="daily",
            retention="2555 days"
        )
        
        self.logger.info("🔒 安全日誌系統啟動")
    
    def _anonymize_data(self, data: str) -> str:
        """匿名化敏感資料"""
        anonymized = data
        
        # 匿名化敏感模式
        for pattern in self.sensitive_patterns:
            anonymized = re.sub(pattern, lambda m: '*' * len(m.group()), anonymized)
        
        return anonymized
    
    def _get_user_hash(self, user_id: str) -> str:
        """生成用戶 ID 的匿名雜湊"""
        return hashlib.sha256(f"{user_id}:security_salt".encode()).hexdigest()[:16]
    
    def _anonymize_ip(self, ip_address: str) -> str:
        """匿名化 IP 地址"""
        parts = ip_address.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.*.* "
        return "***.***.***.**"
    
    def _get_security_level(self, event_type: SecurityEventType) -> SecurityLevel:
        """根據事件類型確定安全級別"""
        level_mapping = {
            SecurityEventType.LOGIN_SUCCESS: SecurityLevel.LOW,
            SecurityEventType.LOGIN_FAILURE: SecurityLevel.MEDIUM,
            SecurityEventType.LOGOUT: SecurityLevel.LOW,
            SecurityEventType.PASSWORD_CHANGE: SecurityLevel.MEDIUM,
            SecurityEventType.PRIVILEGE_ESCALATION: SecurityLevel.HIGH,
            SecurityEventType.DATA_ACCESS: SecurityLevel.MEDIUM,
            SecurityEventType.DATA_EXPORT: SecurityLevel.HIGH,
            SecurityEventType.CONFIGURATION_CHANGE: SecurityLevel.HIGH,
            SecurityEventType.SUSPICIOUS_ACTIVITY: SecurityLevel.HIGH,
            SecurityEventType.UNAUTHORIZED_ACCESS: SecurityLevel.CRITICAL,
            SecurityEventType.SECURITY_VIOLATION: SecurityLevel.CRITICAL,
            SecurityEventType.AUDIT_EVENT: SecurityLevel.MEDIUM,
        }
        return level_mapping.get(event_type, SecurityLevel.MEDIUM)
    
    def _is_suspicious_activity(self, user_id: str, ip_address: str, 
                               event_type: SecurityEventType) -> bool:
        """檢測可疑活動"""
        # 檢查失敗登入嘗試
        if event_type == SecurityEventType.LOGIN_FAILURE:
            key = f"{user_id}:{ip_address}"
            now = datetime.utcnow()
            
            if key not in self.failed_attempts:
                self.failed_attempts[key] = []
            
            # 清理15分鐘前的記錄
            self.failed_attempts[key] = [
                timestamp for timestamp in self.failed_attempts[key]
                if now - timestamp < timedelta(minutes=15)
            ]
            
            self.failed_attempts[key].append(now)
            
            # 15分鐘內超過5次失敗嘗試
            if len(self.failed_attempts[key]) > 5:
                self.suspicious_ips.add(ip_address)
                return True
        
        # 檢查已知可疑 IP
        if ip_address in self.suspicious_ips:
            return True
        
        return False
    
    def log_security_event(self, event_type: SecurityEventType, user_id: str, 
                          ip_address: str, user_agent: str = None, 
                          details: Dict = None, resource: str = None):
        """記錄安全事件"""
        security_level = self._get_security_level(event_type)
        is_suspicious = self._is_suspicious_activity(user_id, ip_address, event_type)
        
        # 準備日誌資料
        log_data = {
            "event_type": event_type.value,
            "security_level": security_level.value,
            "user_id": self._get_user_hash(user_id),
            "ip_address": self._anonymize_ip(ip_address),
            "user_agent": self._anonymize_data(user_agent or ""),
            "resource": resource,
            "timestamp": datetime.utcnow().isoformat(),
            "is_suspicious": is_suspicious,
            "details": details or {}
        }
        
        # 匿名化 details 中的敏感資料
        if details:
            log_data["details"] = {
                k: self._anonymize_data(str(v)) if isinstance(v, str) else v
                for k, v in details.items()
            }
        
        # 根據安全級別選擇日誌級別
        if security_level == SecurityLevel.CRITICAL:
            self.logger.critical(f"🚨 嚴重安全事件: {event_type.value}", extra=log_data)
        elif security_level == SecurityLevel.HIGH:
            self.logger.error(f"⚠️ 高風險安全事件: {event_type.value}", extra=log_data)
        elif security_level == SecurityLevel.MEDIUM:
            self.logger.warning(f"⚡ 中風險安全事件: {event_type.value}", extra=log_data)
        else:
            self.logger.info(f"ℹ️ 安全事件: {event_type.value}", extra=log_data)
        
        # 可疑活動額外處理
        if is_suspicious:
            self._trigger_security_alert(log_data)
    
    def log_audit_event(self, action: str, user_id: str, resource: str, 
                       before_state: Dict = None, after_state: Dict = None,
                       ip_address: str = None):
        """記錄審計事件"""
        audit_data = {
            "event_type": "audit",
            "action": action,
            "user_id": self._get_user_hash(user_id),
            "resource": resource,
            "ip_address": self._anonymize_ip(ip_address) if ip_address else None,
            "before_state": before_state or {},
            "after_state": after_state or {},
            "timestamp": datetime.utcnow().isoformat(),
            "audit_id": hashlib.md5(f"{action}:{user_id}:{resource}:{datetime.utcnow().isoformat()}".encode()).hexdigest()
        }
        
        self.audit_logger.info(f"📋 審計: {action} on {resource}", extra=audit_data)
    
    def _trigger_security_alert(self, security_event: Dict):
        """觸發安全警報"""
        alert_data = {
            "alert_type": "security_incident",
            "severity": "high",
            "event": security_event,
            "alert_time": datetime.utcnow().isoformat(),
            "requires_investigation": True
        }
        
        self.logger.critical("🚨 安全警報觸發", extra=alert_data)
        
        # 在實際環境中，這裡會發送到監控系統
        print(f"🚨 安全警報: {security_event['event_type']} - IP: {security_event['ip_address']}")
    
    def generate_security_report(self, hours: int = 24) -> Dict:
        """生成安全報告"""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        report = {
            "report_period_hours": hours,
            "report_generated": datetime.utcnow().isoformat(),
            "suspicious_ips_count": len(self.suspicious_ips),
            "failed_attempts_count": sum(
                len([t for t in attempts if t > cutoff_time])
                for attempts in self.failed_attempts.values()
            ),
            "security_incidents": [],
            "recommendations": [
                "定期更新密碼政策",
                "啟用多因素驗證",
                "監控異常登入活動",
                "定期安全培訓"
            ]
        }
        
        self.logger.info("📊 安全報告生成", extra=report)
        return report

def demonstrate_security_logging():
    """演示安全日誌功能"""
    print("🔒 安全日誌系統演示")
    print("=" * 50)
    
    security_logger = SecurityLogger()
    
    # 模擬正常登入
    print("1. 模擬正常用戶登入...")
    security_logger.log_security_event(
        event_type=SecurityEventType.LOGIN_SUCCESS,
        user_id="user_123",
        ip_address="192.168.1.100",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        details={"login_method": "password"}
    )
    
    # 模擬失敗登入嘗試
    print("2. 模擬多次失敗登入嘗試...")
    for i in range(6):  # 觸發可疑活動檢測
        security_logger.log_security_event(
            event_type=SecurityEventType.LOGIN_FAILURE,
            user_id="attacker_456",
            ip_address="10.0.0.50",
            user_agent="curl/7.68.0",
            details={"reason": "invalid_password", "attempt": i+1}
        )
    
    # 模擬特權提升
    print("3. 模擬特權提升事件...")
    security_logger.log_security_event(
        event_type=SecurityEventType.PRIVILEGE_ESCALATION,
        user_id="admin_789",
        ip_address="192.168.1.10",
        resource="admin_panel",
        details={"old_role": "user", "new_role": "admin"}
    )
    
    # 模擬資料存取
    print("4. 模擬敏感資料存取...")
    security_logger.log_security_event(
        event_type=SecurityEventType.DATA_ACCESS,
        user_id="user_123",
        ip_address="192.168.1.100",
        resource="customer_database",
        details={"table": "customers", "action": "SELECT", "record_count": 1500}
    )
    
    # 模擬配置變更
    print("5. 模擬系統配置變更...")
    security_logger.log_audit_event(
        action="config_change",
        user_id="admin_789",
        resource="security_settings",
        before_state={"max_login_attempts": 3},
        after_state={"max_login_attempts": 5},
        ip_address="192.168.1.10"
    )
    
    # 模擬資料匯出
    print("6. 模擬大量資料匯出...")
    security_logger.log_security_event(
        event_type=SecurityEventType.DATA_EXPORT,
        user_id="user_123",
        ip_address="192.168.1.100",
        resource="user_reports",
        details={
            "export_format": "CSV",
            "record_count": 10000,
            "contains_pii": True,
            "approval_required": True
        }
    )
    
    # 模擬未授權存取嘗試
    print("7. 模擬未授權存取嘗試...")
    security_logger.log_security_event(
        event_type=SecurityEventType.UNAUTHORIZED_ACCESS,
        user_id="unknown_user",
        ip_address="203.0.113.1",
        resource="admin_api",
        details={"error": "access_denied", "endpoint": "/api/admin/users"}
    )
    
    # 生成安全報告
    print("8. 生成安全報告...")
    report = security_logger.generate_security_report(hours=1)
    
    print("\n📊 安全事件統計:")
    print(f"   - 可疑 IP 數量: {report['suspicious_ips_count']}")
    print(f"   - 失敗嘗試次數: {report['failed_attempts_count']}")
    
    print("\n📁 安全日誌檔案位置:")
    print("   - logs/security/ (安全事件日誌)")
    print("   - logs/audit/ (審計追蹤日誌)")

if __name__ == "__main__":
    demonstrate_security_logging()
