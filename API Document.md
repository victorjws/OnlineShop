# API Document
## Index
* [Product](#product)
  + [/product/list-api/](#listapi)
    - [[GET] 쇼핑몰의 상품목록을 반환합니다.](#listapiget)
  + [/product/detail-api/{pk}/](#detailapi)
    - [[GET] 자세한 상품정보를 반환합니다.](#detailapiget)
  + [/product/category-list-api/](#categorylistapi)
    - [[GET] 카테고리 목록을 반환합니다.](#categorylistapiget)
* [Order](#order)
  + [/order/cart-api/](#cartapi)
    - [[GET] 계정의 장바구니 목록을 반환합니다.](#cartapiget)
    - [[POST] 장바구니에 상품을 추가합니다.](#cartapipost)
    - [[PATCH] 장바구니에 담은 상품의 주문수량을 변경합니다.](#cartapipatch)
    - [[DELETE] 장바구니에 담은 상품을 삭제합니다.](#cartapidelete)
  + [/order/order-api/](#orderapi)
    - [[GET] 결제 완료된 주문 목록을 반환합니다.](#orderapiget)
  + [/order/exist-api/](#existapi)
    - [[GET] 상품이 장바구니에 존재하는지 여부를 반환합니다.](#existapiget)
  + [/order/payments-complete/](#paymentscomplete)
    - [[POST] 결제가 정상적으로 처리되었는지 확인 후 결제 완료 목록에 상품을 추가하고 장바구니에서 삭제합니다. 동시에 상품 재고량도 수정합니다.](#paymentscompletepost)

## Product
### /product/list-api/ <a id="listapi"></a>
#### [GET] 쇼핑몰의 상품목록을 반환합니다. <a id="listapiget"></a>
* Parameter
  
|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|limit_count|None|불러올 상품 목록 개수를 제한할 숫자|query|integer|false|
|category|None|카테고리별 상품 목록|query|string|false|
|page|None|불러올 상품 목록 페이지 번호|query|integer|false|

* Response Class (Status 200)

  * count: 불러온 상품 목록 개수
  * next: 다음 페이지 링크(or null)
  * previous: 이전 페이지 링크(or null)
  * page_links: 페이지가 나뉠 경우 각 페이지 별 정보
    * 1: 페이지 링크. 4 가 true일 경우 숫자 대신 null
    * 2: 페이지 숫자. 4 가 true일 경우 숫자 대신 null
    * 3: 현재 선택된 페이지 여부
    * 4: 페이지 줄임(&hellip) 여부. 페이지가 많을 경우 중간을 ... 으로 생략합니다.
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

```
{
    "count": 0,
    "next": "string",
    "previous": "string",
    "page_links": [
        [
            "string",
            1,
            true,
            true
        ]
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
            "is_discount": true,
            "discount_price": 0
        },
    ]
}
```
### /product/detail-api/{pk}/ <a id="detailapi"></a>
#### [GET] 자세한 상품정보를 반환합니다. <a id="detailapiget"></a>
* Parameter

|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|pk|None|요청할 상품 id|path|integer|true|

* Response Class (Status 200)
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
    "is_discount": true,
    "discount_price": 0
}
```
### /product/category-list-api/ <a id="categorylistapi"></a>
#### [GET] 카테고리 목록을 반환합니다. <a id="categorylistapiget"></a>

* Response Class (Status 200)
  * categories: 상품 카테고리
    * id: 카테고리 id
    * name: 카테고리 이름

```json
[
    {
        "id": 0,
        "name": "string"
    }
]
```
## Order
### /order/cart-api/ <a id="cartapi"></a>
#### [GET] 계정의 장바구니 목록을 반환합니다. <a id="cartapiget"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Response Class (Status 200)
  * id: 사용자 pk
  * customer: 사용자의 정보
    * email: 사용자의 email
    * nickname: 사용자의 nickname
    * shipping_address: 사용자의 주소
  * product: 사용자가 장바구니에 추가한 상품
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
  * quantity: 장바구니에 담은 상품의 개수

```json
[
    {
        "id": 0,
        "customer": {
            "email": "string",
            "nickname": "string",
            "shipping_address": "string"
        },
        "product": {
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
            "is_discount": true,
            "discount_price": 0
        },
        "quantity": 1
    }
]
```
* Response Messages

|HTTP Status Code|Reason|
|:---:|---|
|401|JWT가 전달되지 않았거나 만료된 경우|

#### [POST] 장바구니에 상품을 추가합니다. <a id="cartapipost"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Parameter

|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|product_id|None|상품의 id|json|integer|true|
|quantity|None|상품 주문 수량|json|integer|true|

```json
{
	"product_id": 0,
	"quantity": 0
}
```

#### [PATCH] 장바구니에 담은 상품의 주문수량을 변경합니다. <a id="cartapipatch"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Parameter
  
|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|product_id|None|상품의 id|json|integer|true|
|quantity|None|상품 주문 수량|json|integer|true|

다수의 상품을 한번에 업데이트하려는 경우 아래와 같은 형식으로 데이터를 전달하면 됩니다.
```json
[
    {
        "product_id": 0,
        "quantity": 0
    },
    {
        "product_id": 0,
        "quantity": 0
    }
]
```
* Response Class (Status 200)

```json
"update complete"
```
또는
```json
"update failed"
```
* Response Messages

|HTTP Status Code|Reason|
|:---:|---|
|401|JWT가 전달되지 않았거나 만료된 경우|

#### [DELETE] 장바구니에 담은 상품을 삭제합니다. <a id="cartapidelete"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Parameter

|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|product_id|None|삭제할 상품 id|json|integer|true|

```json
{
    "product_id": 0
}
```
* Response Class (Status 200)

```json
"delete complete"
```
또는
```json
"delete failed"
```
* Response Messages

|HTTP Status Code|Reason|
|:---:|---|
|401|JWT가 전달되지 않았거나 만료된 경우|

### /order/order-api/ <a id="orderapi"></a>
#### [GET] 결제 완료된 주문 목록을 반환합니다. <a id="orderapiget"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Response Class (Status 200)
  * id: 사용자 pk
  * customer: 사용자의 정보
    * email: 사용자의 email
    * nickname: 사용자의 nickname
    * shipping_address: 사용자의 주소
  * product: 사용자가 장바구니에 추가한 상품
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
  * quantity: 장바구니에 담은 상품의 개수
  * order_date: 결제 완료한 시간
```json
[
    {
        "id": 0,
        "customer": {
            "email": "string",
            "nickname": "string",
            "shipping_address": "string"
        },
        "product": {
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
            "is_discount": true,
            "discount_price": 0
        },
        "quantity": 0,
        "order_date": "string"
    }
]
```
* Response Messages

|HTTP Status Code|Reason|
|:---:|---|
|401|JWT가 전달되지 않았거나 만료된 경우|

### /order/exist-api/ <a id="existapi"></a>
#### [GET] 상품이 장바구니에 존재하는지 여부를 반환합니다. <a id="existapiget"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Parameter

|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|product_id|None|상품의 id|query|integer|true|

* Response Class (Status 200)
  * result: 장바구니에 존재하는지 여부
```json
{
    "result": true
}
```
* Response Messages

|HTTP Status Code|Reason|
|:---:|---|
|401|JWT가 전달되지 않았거나 만료된 경우|

### /order/payments-complete/ <a id="paymentscomplete"></a>
#### [POST] 결제가 정상적으로 처리되었는지 확인 후 결제 완료 목록에 상품을 추가하고 장바구니에서 삭제합니다. 동시에 상품 재고량도 수정합니다. <a id="paymentscompletepost"></a>
해당 API는 Header의 Authorization 항목에 'Bearer {JWT}'가 필요합니다.
* Parameter

|Parameter|Default value|Description|Param type|Data type|Required|
|---|---|---|---|---|---|
|imp_uid|None|Iamport에서 결제 정보를 확인할 때 필요한 imp_uid|json|string|true|

```json
{
    "imp_uid": "string"
}
```
* Response Class (Status 200)
  * status: 처리 결과
```json
{
    "status": "success"
}
```
또는
```json
{
    "status": "failed"
}
```
* Response Messages

|HTTP Status Code|Reason|
|:---:|---|
|401|JWT가 전달되지 않았거나 만료된 경우|
