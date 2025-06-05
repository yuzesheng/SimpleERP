from rest_framework import serializers

from orders.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name',read_only=True)
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id','product','product_name','quantity','item_total']
    def get_item_total(self,obj):
        return obj.get_item_total()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True)
    total_price = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id','customer','customer_name','status','items','total_price','created_at']
        read_only_fields = ['owner','created_at','total_price']

    def create(self,validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(owner=self.context['request'].user,**validated_data)
        total = 0
        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            OrderItem.objects.create(order = order,product = product,quantity=quantity)
            total += product.price * quantity

        order.total_price = total
        order.save()
        return order
