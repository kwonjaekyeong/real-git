# pip install cx_oracle 모듈설치
import cx_Oracle as oci

# 접속하기(아이디/암호@서버주소:포트번호/SID)
conn = oci.connect('admin/1234@192.168.99.100:32764/xe', encoding="utf-8")
print(conn) # 확인

# # 커서 생성
# cursor = conn.cursor()

# # SELECT
# sql = "SELECT * FROM MEMBER"
# cursor.execute(sql)
# data = cursor.fetchall()  #[(),(),()]
# print(data)

# # INSERT
# sql = """
#     INSERT INTO MEMBER(ID, PW, NAME, AGE, JOINDATE)
#     VALUES(:1, :2, :3, :4, SYSDATE)
#     """

# arr = ['a1', 'a1', '홍길동', 33]
# cursor.execute(sql, arr)
# conn.commit()
