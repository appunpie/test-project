import sys
import hashlib
import json

def main():
    seed = 'zdfvadfv'
    n = int(3)
    if n == 0:
        return 1
    elif n == 2:
        return 2
    elif n % 2 == 0:
        return main(n-1) + main(n-2) + main(n-3) + main(n-4)
    else:
        return askServer(seed, n)

def askServer(seed, n):
    data = f'{seed}:{n}'
    #print(data)
    hash_value = hashlib.sha256(data.encode()).hexdigest()  #ハッシュ値を取得
    hash_int = int(hash_value[:8], 16)  #頭文字8桁でも十分に区別が可能なので8桁にした
    print((hash_int % 300) + 1)  #300で割った余りから数字を指定


    

if __name__ == '__main__':
    main()

#わかりませんでした
#試験終了後に詳しく調べて、できるだけ説明できるようにしようと思います。