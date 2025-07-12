#!/usr/bin/env python3
"""
📋 08_enterprise/compliance.py
合規性管理範例

這個範例展示了如何實現企業級的合規性管理，
包含 GDPR/CCPA 合規、日誌保留政策、數據匿名化和合規審計支援。
"""

import hashlib
import json
import re
from typing import Dict, List, Optional, Set, Any
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from pretty_loguru import create_logger

class ComplianceFramework(Enum):
    """合規框架"""
    GDPR = "gdpr"  # 歐盟一般資料保護規定
    CCPA = "ccpa"  # 加州消費者隱私法
    SOX = "sox"    # 薩班斯-奧克斯利法案
    HIPAA = "hipaa" # 健康保險可攜與責任法案
    PCI_DSS = "pci_dss" # 支付卡行業數據安全標準

class DataCategory(Enum):
    """資料類別"""
    PERSONAL_DATA = "personal_data"
    FINANCIAL_DATA = "financial_data"
    HEALTH_DATA = "health_data"
    SYSTEM_LOGS = "system_logs"
    SECURITY_LOGS = "security_logs"
    AUDIT_LOGS = "audit_logs"
    TRANSACTION_LOGS = "transaction_logs"

@dataclass
class RetentionPolicy:
    """資料保留政策"""
    category: DataCategory
    retention_period: timedelta
    framework: ComplianceFramework
    description: str
    anonymization_required: bool = False
    encryption_required: bool = False

class ComplianceManager:
    """合規性管理器"""
    
    def __init__(self):
        # 定義保留政策
        self.retention_policies = {
            DataCategory.PERSONAL_DATA: RetentionPolicy(
                category=DataCategory.PERSONAL_DATA,
                retention_period=timedelta(days=1095),  # 3年 (GDPR)
                framework=ComplianceFramework.GDPR,
                description="個人資料根據 GDPR 要求保留3年",
                anonymization_required=True,
                encryption_required=True
            ),
            DataCategory.FINANCIAL_DATA: RetentionPolicy(
                category=DataCategory.FINANCIAL_DATA,
                retention_period=timedelta(days=2555),  # 7年 (SOX)
                framework=ComplianceFramework.SOX,
                description="財務資料根據 SOX 法案保留7年",
                encryption_required=True
            ),
            DataCategory.SECURITY_LOGS: RetentionPolicy(
                category=DataCategory.SECURITY_LOGS,
                retention_period=timedelta(days=2555),  # 7年
                framework=ComplianceFramework.SOX,
                description="安全日誌保留7年用於審計",
                encryption_required=True
            ),
            DataCategory.SYSTEM_LOGS: RetentionPolicy(
                category=DataCategory.SYSTEM_LOGS,
                retention_period=timedelta(days=90),  # 90天
                framework=ComplianceFramework.GDPR,
                description="系統日誌保留90天"
            ),
            DataCategory.AUDIT_LOGS: RetentionPolicy(
                category=DataCategory.AUDIT_LOGS,
                retention_period=timedelta(days=2555),  # 7年
                framework=ComplianceFramework.SOX,
                description="審計日誌永久保留用於合規檢查",
                encryption_required=True
            )
        }
        
        # 敏感資料模式
        self.sensitive_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'passport': r'\b[A-Z]{1,2}\d{7,9}\b'
        }
        
        # 建立合規日誌記錄器
        self.logger = create_logger(
            name="compliance_manager",
            log_path="logs/compliance",
            level="INFO",
            rotation="daily",
            retention="permanent"  # 合規日誌永久保留
        )
        
        self.data_processor_logger = create_logger(
            name="data_processor",
            log_path="logs/data_processing",
            level="INFO",
            rotation="daily",
            retention="7 years"
        )
        
        self.logger.info("📋 合規性管理系統啟動")
    
    def detect_sensitive_data(self, text: str) -> Dict[str, List[str]]:
        """檢測敏感資料"""
        detected = {}
        
        for data_type, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                detected[data_type] = matches
        
        return detected
    
    def anonymize_field(self, value: str, field_type: str) -> str:
        """匿名化特定欄位"""
        if field_type == 'email':
            if '@' in value:
                local, domain = value.split('@', 1)
                return f"{local[:2]}***@{domain}"
        elif field_type == 'phone':
            return '***-***-' + value[-4:] if len(value) >= 4 else '***'
        elif field_type == 'credit_card':
            return '****-****-****-' + value[-4:] if len(value) >= 4 else '****'
        elif field_type == 'ssn':
            return '***-**-' + value[-4:] if len(value) >= 4 else '***'
        else:
            # 通用匿名化：顯示前2位和後2位
            if len(value) > 4:
                return value[:2] + '*' * (len(value) - 4) + value[-2:]
            else:
                return '*' * len(value)
    
    def anonymize_log_record(self, log_record: Dict[str, Any]) -> Dict[str, Any]:
        """匿名化日誌記錄"""
        anonymized_record = log_record.copy()
        
        # 遞迴處理所有字串值
        def anonymize_value(value):
            if isinstance(value, str):
                sensitive_data = self.detect_sensitive_data(value)
                anonymized_value = value
                
                for data_type, matches in sensitive_data.items():
                    for match in matches:
                        anonymized_match = self.anonymize_field(match, data_type)
                        anonymized_value = anonymized_value.replace(match, anonymized_match)
                
                return anonymized_value
            elif isinstance(value, dict):
                return {k: anonymize_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [anonymize_value(item) for item in value]
            else:
                return value
        
        anonymized_record = anonymize_value(anonymized_record)
        anonymized_record['_anonymized'] = True
        anonymized_record['_anonymization_timestamp'] = datetime.utcnow().isoformat()
        
        return anonymized_record
    
    def apply_retention_policy(self, category: DataCategory) -> Dict[str, Any]:
        """應用資料保留政策"""
        if category not in self.retention_policies:
            raise ValueError(f"未定義的資料類別: {category}")
        
        policy = self.retention_policies[category]
        cutoff_date = datetime.utcnow() - policy.retention_period
        
        retention_action = {
            "action": "data_retention_policy_applied",
            "category": category.value,
            "framework": policy.framework.value,
            "retention_period_days": policy.retention_period.days,
            "cutoff_date": cutoff_date.isoformat(),
            "description": policy.description,
            "anonymization_required": policy.anonymization_required,
            "encryption_required": policy.encryption_required,
            "applied_at": datetime.utcnow().isoformat()
        }
        
        self.logger.info(f"📅 應用保留政策: {category.value}", extra=retention_action)
        return retention_action
    
    def log_data_processing_activity(self, activity: str, data_subject: str, 
                                   data_types: List[str], legal_basis: str,
                                   purpose: str, retention_period: str = None):
        """記錄資料處理活動 (GDPR Article 30)"""
        processing_record = {
            "activity": activity,
            "data_subject": hashlib.sha256(data_subject.encode()).hexdigest()[:16],
            "data_types": data_types,
            "legal_basis": legal_basis,
            "purpose": purpose,
            "retention_period": retention_period,
            "processing_timestamp": datetime.utcnow().isoformat(),
            "compliance_framework": ComplianceFramework.GDPR.value,
            "record_id": hashlib.md5(f"{activity}:{data_subject}:{datetime.utcnow()}".encode()).hexdigest()
        }
        
        self.data_processor_logger.info(f"📊 資料處理活動: {activity}", extra=processing_record)
    
    def handle_data_subject_request(self, request_type: str, data_subject: str, 
                                   requested_data: List[str] = None):
        """處理資料主體請求 (GDPR Rights)"""
        request_record = {
            "request_type": request_type,  # access, rectification, erasure, portability
            "data_subject": hashlib.sha256(data_subject.encode()).hexdigest()[:16],
            "requested_data": requested_data or [],
            "request_timestamp": datetime.utcnow().isoformat(),
            "status": "received",
            "response_deadline": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "compliance_framework": ComplianceFramework.GDPR.value,
            "request_id": hashlib.md5(f"{request_type}:{data_subject}:{datetime.utcnow()}".encode()).hexdigest()
        }
        
        self.logger.info(f"📮 資料主體請求: {request_type}", extra=request_record)
        
        # 根據請求類型進行特殊處理
        if request_type == "erasure":  # 被遺忘權
            self._process_erasure_request(request_record)
        elif request_type == "access":  # 存取權
            self._process_access_request(request_record)
    
    def _process_erasure_request(self, request_record: Dict):
        """處理資料刪除請求"""
        erasure_log = {
            "action": "data_erasure",
            "request_id": request_record["request_id"],
            "data_subject": request_record["data_subject"],
            "erasure_timestamp": datetime.utcnow().isoformat(),
            "legal_basis": "GDPR Article 17 - Right to erasure",
            "verification_required": True
        }
        
        self.logger.warning("🗑️ 資料刪除請求處理", extra=erasure_log)
    
    def _process_access_request(self, request_record: Dict):
        """處理資料存取請求"""
        access_log = {
            "action": "data_access",
            "request_id": request_record["request_id"],
            "data_subject": request_record["data_subject"],
            "access_timestamp": datetime.utcnow().isoformat(),
            "legal_basis": "GDPR Article 15 - Right of access",
            "data_provided": True
        }
        
        self.logger.info("👁️ 資料存取請求處理", extra=access_log)
    
    def conduct_compliance_audit(self, framework: ComplianceFramework) -> Dict[str, Any]:
        """進行合規性審計"""
        audit_report = {
            "audit_type": "compliance_audit",
            "framework": framework.value,
            "audit_timestamp": datetime.utcnow().isoformat(),
            "audit_period": "last_30_days",
            "findings": [],
            "recommendations": [],
            "compliance_score": 0,
            "audit_id": hashlib.md5(f"audit:{framework.value}:{datetime.utcnow()}".encode()).hexdigest()
        }
        
        # 模擬審計發現
        if framework == ComplianceFramework.GDPR:
            audit_report["findings"] = [
                "資料處理活動記錄完整",
                "匿名化程序正常運作",
                "保留政策已正確實施"
            ]
            audit_report["recommendations"] = [
                "定期檢查資料主體請求處理時間",
                "加強資料處理人員培訓",
                "更新隱私政策文件"
            ]
            audit_report["compliance_score"] = 95
        
        elif framework == ComplianceFramework.SOX:
            audit_report["findings"] = [
                "財務日誌保留期符合要求",
                "存取控制適當",
                "變更管理程序完整"
            ]
            audit_report["recommendations"] = [
                "強化資料庫存取監控",
                "實施更嚴格的變更審批流程"
            ]
            audit_report["compliance_score"] = 92
        
        self.logger.info(f"📋 合規性審計完成: {framework.value}", extra=audit_report)
        return audit_report
    
    def generate_compliance_report(self, frameworks: List[ComplianceFramework] = None) -> Dict[str, Any]:
        """生成綜合合規報告"""
        if frameworks is None:
            frameworks = [ComplianceFramework.GDPR, ComplianceFramework.SOX]
        
        compliance_report = {
            "report_type": "comprehensive_compliance_report",
            "report_timestamp": datetime.utcnow().isoformat(),
            "reporting_period": "monthly",
            "frameworks_covered": [f.value for f in frameworks],
            "retention_policies": {
                cat.value: {
                    "retention_period_days": policy.retention_period.days,
                    "framework": policy.framework.value,
                    "anonymization_required": policy.anonymization_required,
                    "encryption_required": policy.encryption_required
                }
                for cat, policy in self.retention_policies.items()
            },
            "data_processing_activities_count": 150,  # 模擬數據
            "data_subject_requests_count": 12,
            "compliance_violations": 0,
            "overall_compliance_score": 94,
            "next_audit_date": (datetime.utcnow() + timedelta(days=90)).isoformat()
        }
        
        self.logger.info("📊 綜合合規報告生成", extra=compliance_report)
        return compliance_report

def demonstrate_compliance_management():
    """演示合規性管理功能"""
    print("📋 合規性管理系統演示")
    print("=" * 50)
    
    compliance_manager = ComplianceManager()
    
    # 1. 演示敏感資料檢測和匿名化
    print("1. 敏感資料檢測和匿名化...")
    sample_data = {
        "user_email": "john.doe@example.com",
        "phone": "555-123-4567",
        "credit_card": "4532-1234-5678-9012",
        "message": "請聯繫我 john.doe@example.com 或致電 555-123-4567"
    }
    
    sensitive_detected = compliance_manager.detect_sensitive_data(str(sample_data))
    print(f"   檢測到敏感資料: {list(sensitive_detected.keys())}")
    
    anonymized_data = compliance_manager.anonymize_log_record(sample_data)
    print(f"   匿名化後: {anonymized_data['user_email']}")
    
    # 2. 應用資料保留政策
    print("\n2. 應用資料保留政策...")
    for category in [DataCategory.PERSONAL_DATA, DataCategory.FINANCIAL_DATA, DataCategory.SECURITY_LOGS]:
        policy_result = compliance_manager.apply_retention_policy(category)
        print(f"   {category.value}: 保留 {policy_result['retention_period_days']} 天")
    
    # 3. 記錄資料處理活動
    print("\n3. 記錄資料處理活動...")
    compliance_manager.log_data_processing_activity(
        activity="user_registration",
        data_subject="user123@example.com",
        data_types=["email", "name", "phone"],
        legal_basis="consent",
        purpose="提供服務",
        retention_period="3_years"
    )
    
    # 4. 處理資料主體請求
    print("\n4. 處理資料主體請求...")
    compliance_manager.handle_data_subject_request(
        request_type="access",
        data_subject="user123@example.com",
        requested_data=["profile_data", "transaction_history"]
    )
    
    compliance_manager.handle_data_subject_request(
        request_type="erasure",
        data_subject="deleted_user@example.com"
    )
    
    # 5. 進行合規性審計
    print("\n5. 進行合規性審計...")
    gdpr_audit = compliance_manager.conduct_compliance_audit(ComplianceFramework.GDPR)
    sox_audit = compliance_manager.conduct_compliance_audit(ComplianceFramework.SOX)
    
    print(f"   GDPR 合規分數: {gdpr_audit['compliance_score']}/100")
    print(f"   SOX 合規分數: {sox_audit['compliance_score']}/100")
    
    # 6. 生成綜合合規報告
    print("\n6. 生成綜合合規報告...")
    comprehensive_report = compliance_manager.generate_compliance_report()
    print(f"   整體合規分數: {comprehensive_report['overall_compliance_score']}/100")
    print(f"   涵蓋框架: {', '.join(comprehensive_report['frameworks_covered'])}")
    
    print("\n📁 合規性日誌檔案位置:")
    print("   - logs/compliance/ (合規管理日誌)")
    print("   - logs/data_processing/ (資料處理活動日誌)")

if __name__ == "__main__":
    demonstrate_compliance_management()