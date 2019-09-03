# API Document
## Product
### /product/list-api/
[GET] 쇼핑몰의 상품목록을 불러옵니다.
* Parameter
  
|Parameter|Defaul value|Description|Param type|Data type|
|---|---|---|---|---|
|limit_count|None|불러올 상품 목록 개수를 제한할 숫자|query|integer|
|category|None|카테고리별 상품 목록|query|string|
|page|None|불러올 상품 목록 페이지|query|integer|

  * Response Class (Status 200)

    * count: 불러온 상품 목록 개수
    * next: 다음 페이지 링크(or null)
    * previous: 이전 페이지 링크(or null)
    * page_links: 페이지가 나뉠 경우 각 페이지 별 정보
      * 1: 페이지 링크
      * 2: 페이지 숫자
      * 3: 현재 선택된 페이지 여부
      * 4: 페이지 줄임(&hellip) 여부
    * results: 가져온 상품 정보
      * id: 상품 id
      * categories: 상품 카테고리
        * id: 카테고리 id
        * name: 카테고리 이름
      * name: 상품 이름
      * price: 상품 가격
      * picture: 상품 이미지 경로
      * description: 상품 설명
      * stock: 상품 재고
      * register_date: 상품 등록 시간
      * is_discount: 상품 할인 여부
      * discount_price: 상품 할인 후 가격(or null)

```json
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "page_links": [
        [
            "string",
            1,
            true,
            false
        ],
    ],
    "results": [
        {
            "id": 0,
            "categories": [
                {
                    "id": 0,
                    "name": "string"
                }
            ],
            "name": "string",
            "price": 0,
            "picture": "string",
            "description": "string",
            "stock": 0,
            "register_date": "string",
            "is_discount": false,
            "discount_price": 0
        },
    ]
}
```
