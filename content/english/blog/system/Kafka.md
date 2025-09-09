---
title: "Kafka"
meta_title: "Kafka"
description: "Giới thiệu về kiến trúc truyền thống và kiến trúc phân tán, sự ra đời của Kafka"
date: 2025-08-09
image: "/images/image-placeholder.png"
categories: ["system", "architechture"]
author: "Nagih"
tags: ["kafka"]
draft: false
---
Giới thiệu về kiến trúc truyền thống và kiến trúc phân tán, sự ra đời của Kafka
<!--more-->
# KAFKA ĐƯỢC DÙNG KHI NÀO ?
### Kiến trúc truyền thống - Lập trình nối tiếp

![Image Description](/images/Pasted%20image%2020250809165924.png)

**Các function quá lệ thuộc vào nhau:** Nếu 1 ngày nào đó, tính năng update cart của 1 nhân viên B bị lỗi thì khi user save order -> update cart nhưng bị lỗi ở đây và trả về lỗi, thực tế nếu hệ thống bỏ qua bước này và cho tới bước update inventory thì có được hay không ? Thực tế, mọi trang thương mại điện tử hiện nay đều có thể xử lý lỗi thành công, **miễn là cho user có trải nghiệm tốt là được**. Nếu xảy ra lỗi. Các hệ thống sẽ trả cho user phần bù đắp thiệt hại cho user (1 vourcher chẳng hạn) chứ không nên để cho user đặt hàng không thành công.

**Trong hình ảnh tiếp theo, tôi đã cung cấp thêm thời gian phản hồi, có thể thấy mỗi 1 request sẽ mất 150ms** 

![Image Description](/images/Pasted%20image%2020250809171312.png)


**Giả sử nhân viên B phụ trách tính năng update cart nhưng code yếu thì làm sao ? Tức là tính năng update cart được tính toán nhiều quá, không hiệu quả, và kết quả là bị tắc đường ở đó.** Và tất nhiên hệ thống phải đồng bộ. Chẳng hạn khi có 10.000 users bị tắc nghẽn ở đó thì phải làm như thế nào ?

![Image Description](/images/Pasted%20image%2020250809171727.png)

**Và một ngày nào đó, lượng users tăng cao, và cần thêm tính năng mới - Thống kê.** Tính năng này thống kê điểm tích lũy cho user để có thể tặng quà cho những người mua hàng nhiều nhất, tích điểm,... Thì khi thêm 1 tính năng bất kỳ, đồng nghĩa với việc sẽ tăng thêm thời gian phản hồi, nguy cơ tăng lỗi cũng sẽ cao hơn

### Kiến trúc phân tán

![Image Description](/images/Pasted%20image%2020250809172709.png)

Có thể thấy, tất cả các order đều được đẩy vào **Message Queue**, và ngay lập tức trả về response cho user, không cần quan tâm tới những tác vụ còn lại. Và tất nhiên các tác vụ update cart, update inventory, save payment, save shopping vẫn được tiến hành và được tiến hành theo đúng trình tự.

**Và nhắc lại trường hợp khi nãy, giả sử tính năng update inventory bị lỗi thì chuyện gì sẽ xảy ra?** Điều đầu tiên là sẽ không ảnh hưởng tới trải nghiệm người dùng, tiếp theo là message queue có cơ chế tự động sửa lỗi những message bị error, nếu cố gắng sửa đổi trong vòng (10) lần mà không thành công, khi đó sẽ đưa con người vào trực tiếp tham gia quá trình sửa đổi này

**Tỉ lệ phản hồi thay vì 150ms như kiến trúc truyền thống thì sẽ chỉ mất 20ms + 5ms từ save order tới message queue, ngay lập tức phản hồi tới user**


![Image Description](/images/Pasted%20image%2020250809173646.png)

**Trong kiến trúc phân tán, ta có thể quy định hệ thống làm việc với cường độ 100 orders/time, đến khi nào order hết trong MQ**, hay có thể nói là chỉ chỉ đưa cho 100 reqs để làm mà thôi, không được vội vàng, còn lại phải xếp hàng lần lượt, cứ như vậy cho đến hết.

**Và bây giờ, nếu lượng users tăng cao và cần thêm tính năng mới thì cũng không hề ảnh hưởng tới dây chuyền sản xuất**

---

*Nếu thấy hay, hãy để lại cho mình 1 comment xuống phía dưới để mình có động lực viết các blog chất lượng tiếp theo nhé!*