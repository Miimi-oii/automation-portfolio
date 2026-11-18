# Automation Portfolio

6 ตัวอย่างงาน integration/automation สำหรับ Upwork portfolio.

| # | Project | ใช้แก้ปัญหา |
|---|---------|-------------|
| 1 | [scraper-to-sheet](01-scraper-to-sheet) | ดึงข้อมูลสินค้าจากหน้าเว็บ (Shopee/Lazada ฯลฯ) ลง Google Sheet อัตโนมัติ |
| 2 | [api-webhook-sync](02-api-webhook-sync) | รับ webhook จากระบบหนึ่ง แปลงข้อมูล ส่งเข้าอีกระบบผ่าน API พร้อม retry/fail-log/Slack alert |
| 3 | [scheduled-report-bot](03-scheduled-report-bot) | ดึงข้อมูล สรุปรายงาน ส่งเข้า LINE/email ตามรอบเวลา |
| 4 | [reporting-dashboard](04-reporting-dashboard) | สรุปข้อมูลจาก pipeline เป็น live dashboard (KPI + กราฟ) |
| 5 | [airtable-n8n-sync](05-airtable-n8n-sync) | sync lead เข้า Airtable แบบ dedupe + linked record สไตล์ n8n workflow |
| 6 | [tracker-dashboard](06-tracker-dashboard) | status tracker + dashboard พร้อม overdue flag อัตโนมัติ |

แต่ละโฟลเดอร์มี `README.md` อธิบาย setup + run + pitch สำหรับ proposal

**common/** — module ที่ใช้ซ้ำข้ามโปรเจกต์ (`retry_client.py`: retry+backoff, fail-log, Slack alert) project #2 import ใช้งานจริงแล้ว

## Next step
- Push ขึ้น GitHub (repo แยกหรือ monorepo นี้ก็ได้)
- ใส่ screenshot/demo output ใน README ของแต่ละตัว
- ใช้ 3 ตัวนี้เป็น portfolio link ใน Upwork profile
