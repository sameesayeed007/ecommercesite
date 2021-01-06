from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from Intense.models import Ticket, TicketReplies, User, Order, Product, ProductImpression, DeliveryArea, DeliveryLocation, DeliveryInfo,APIs,product_delivery_area,OrderDetails
from .serializers import TicketSerializer, TicketRepliesSerializer, AreaSerializer, LocationSerializer, DeliverySerializer,ApienabledisableSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
from django.contrib.sites.models import Site


@api_view(['GET', ])
def delivery_statistics(request):


	delivered = 0
	pending = 0
	cancelled = 0 
	total = 0 


	try:

		all_orders = Order.objects.filter(checkout_status=True,admin_status="Confirmed")

	except:

		all_orders = None 

	print(all_orders)


	if all_orders:

		all_orders_lists = list(all_orders.values_list('id', flat=True))
		total = int(len(all_orders_lists))

	else:

		total = 0 



	try:

		delivered_orders = Order.objects.filter(delivery_status="Received",checkout_status=True,admin_status="Confirmed")

	except:

		delivered_orders = None 


	if delivered_orders:

		delivered_orders_lists = list(delivered_orders.values_list('id', flat=True))
		delivered = int(len(delivered_orders_lists))
		# format(sum_total, '0.2f')
		delivered = float((delivered / total)*100)
		# delivered = (delivered , '0.2f')

	else:

		delivered = 0 


	try:

		delivered_orders = Order.objects.filter(delivery_status="To ship",checkout_status=True,admin_status="Confirmed")

	except:

		delivered_orders = None 


	if delivered_orders:

		delivered_orders_lists = list(delivered_orders.values_list('id', flat=True))
		pending = int(len(delivered_orders_lists))
		pending = float((pending / total)*100)
		# pending = (pending , '0.2f' )

	else:

		pending = 0 


	try:

		delivered_orders = Order.objects.filter(delivery_status="Cancelled",checkout_status=True)

	except:

		delivered_orders = None 


	if delivered_orders:

		delivered_orders_lists = list(delivered_orders.values_list('id', flat=True))
		cancelled = int(len(delivered_orders_lists))
		cancelled = float((cancelled / total)*100)
		# cancelled = (cancelled,'0.2f')

	else:

		cancelled = 0 


	return JsonResponse({'success':'True','message':'The values are shown','delivered':delivered,'pending':pending,'cancelled':cancelled})




@api_view(['GET', ])
def order_statistics(request):


	delivered = 0
	pending = 0
	cancelled = 0 
	total = 0 




	try:

		all_orders = Order.objects.filter(checkout_status=True,admin_status="Confirmed")

	except:

		all_orders = None 

	print(all_orders)


	if all_orders:

		all_orders_lists = list(all_orders.values_list('id', flat=True))
		total = int(len(all_orders_lists))

	else:

		total = 0 



	try:

		delivered_orders = Order.objects.filter(delivery_status="Received",order_status="Paid",checkout_status=True,admin_status="Confirmed")

	except:

		delivered_orders = None 


	if delivered_orders:

		delivered_orders_lists = list(delivered_orders.values_list('id', flat=True))
		delivered = int(len(delivered_orders_lists))
		# format(sum_total, '0.2f')
		delivered = float((delivered / total)*100)
		# delivered = (delivered , '0.2f')

	else:

		delivered = 0 


	try:

		delivered_orders = Order.objects.filter(delivery_status="To ship",order_status="Unpaid",checkout_status=True,admin_status="Confirmed")|Order.objects.filter(delivery_status="To ship",order_status="Paid",checkout_status=True,admin_status="Confirmed")

	except:

		delivered_orders = None 


	if delivered_orders:

		delivered_orders_lists = list(delivered_orders.values_list('id', flat=True))
		pending = int(len(delivered_orders_lists))
		pending = float((pending / total)*100)
		# pending = (pending , '0.2f' )

	else:

		pending = 0 


	try:

		delivered_orders = Order.objects.filter(delivery_status="Cancelled",order_status="Unpaid",checkout_status=True)

	except:

		delivered_orders = None 


	if delivered_orders:

		delivered_orders_lists = list(delivered_orders.values_list('id', flat=True))
		cancelled = int(len(delivered_orders_lists))
		cancelled = float((cancelled / total)*100)
		# cancelled = (cancelled,'0.2f')

	else:

		cancelled = 0 


	return JsonResponse({'success':'True','message':'The values are shown','completed':delivered,'processing':pending,'cancelled':cancelled})















@api_view(['GET', ])
def dashboard(request):

	total_orders = 0
	total_customers = 0
	total_sellers = 0
	total_staff = 0

	current_date = timezone.now().date()

	try:

		orders = Order.objects.filter(
		    checkout_status=True, ordered_date=current_date)

	except:

		orders = None

	print(orders)

	if orders:

		print("ashtese")

		order_list = list(orders.values_list('id', flat=True).distinct())
		total_orders = len(order_list)

	try:

		orders_customers = Order.objects.filter(checkout_status=True)

	except:

		orders_customers = None

	if orders_customers:

		verified_customers = 0
		non_verified_customers = 0

		customer_list = list(orders_customers.values_list(
		    'user_id', flat=True).distinct())
		# print(customer_list)
		if -1 in customer_list:
			# print("customer eu minus")
			verified_customers = len(customer_list)-1
		else:
			verified_customers = len(customer_list)

		# print(verified_customers)
		non_customer_list = list(orders_customers.values_list(
		    'non_verified_user_id', flat=True).distinct())
		if -1 in non_customer_list:
			# print("noncustomer eu minus")
			non_verified_customers = len(non_customer_list)-1
		else:
			non_verified_customers = len(non_customer_list)

		# print(non_verified_customers)
		# print("dagwdufdfg")

		# print(customer_list)
		# print(non_customer_list)

		# print(verfied_customers)
		# print(non_verified_customers)

		total_customers = verified_customers + non_verified_customers

	try:

		sellers = User.objects.filter(is_suplier=True)

	except:

		sellers = None

	if sellers:

		sellers_list = list(sellers.values_list('id', flat=True).distinct())

		total_sellers = len(sellers_list)

	try:

		staff = User.objects.filter(is_staff=True)

	except:

		staff = None

	if staff:

		staff_list = list(staff.values_list('id', flat=True).distinct())

		total_staff = len(staff_list)

	data = {
				'orders': total_orders,
				'total_customers': total_customers,
				'total_sellers': total_sellers,
				'total_staff': total_staff

			}

	return JsonResponse(
			{
				'success': True,
				'message': 'Data is shown below',
				'data': data
			}, safe=False)


# shows all the tickets and the replies of that specific ticket
# This is for the admin
@api_view(['GET', ])
def ticket_list(request):

	try:
		tickets = Ticket.objects.all()
		ticketserializer = TicketSerializer(tickets, many=True)

		return JsonResponse(
			{
				'success': True,
				'message': 'Data has been retrieved successfully',
				'data': ticketserializer.data
			}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'There are no tickets'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
def unattended_ticket_list(request):

	ticket_count = 0

	try:
		tickets = Ticket.objects.filter(is_attended=False)

	except:
		tickets = None

	if tickets:

		ticket_lists = list(tickets.values_list('id', flat=True).distinct())

		ticket_count = len(ticket_lists)

		ticketserializer = TicketSerializer(tickets, many=True)
		return JsonResponse(
			{
				'success': True,
				'message': 'Data has been retrieved successfully',
				'ticket_count': ticket_count,
				'data': ticketserializer.data
			}, safe=False)

	else:

		return JsonResponse(
			{
				'success': False,
				'message': 'No data is available',
				'ticket_count': ticket_count,
				'data': {}
			}, safe=False)


@api_view(['GET', ])
def seller_dashboard(request, user_id):

	total_sales = 0
	total_customers = 0
	current_products = 0
	cancelled_products = 0
	total_prods = 0

	current_date = timezone.now().date()

	try:

		products = Product.objects.filter(
		    seller=user_id, product_admin_status="Confirmed")

	except:

		products = None

	if products:

		product_list = list(products.values_list('id', flat=True).distinct())
		total_products = int(len(product_list))
		current_products = total_products

		for i in range(len(product_list)):

			try:
				p_imp = ProductImpression.objects.filter(product_id=product_list[i]).last()
				print(p_imp)

			except:

				p_imp = None

			if p_imp:

				total_sales += p_imp.sales_count

				total_verified_customers = len(p_imp.users)
				total_non_customers = len(p_imp.non_verified_user)

				total_customers += int(total_verified_customers) + int(total_non_customers)

			else:

				total_sales = total_sales
				total_customers = total_customers

	else:
		print("ashteset na")

		total_sales = 0
		total_customers = 0
		current_products = 0

	try:

		product = Product.objects.filter(
		    seller=user_id, product_admin_status="Cancelled")

	except:

		product = None

	if product:

		product_lists = list(product.values_list('id', flat=True).distinct())
		total_product = int(len(product_lists))
		cancelled_products = total_product

	else:

		cancelled_products = 0

	data = {'total_sales': total_sales, 'total_customers': total_customers,
	    'current_products': current_products, 'cancelled_products': cancelled_products}

	return JsonResponse({'success': True, 'message': 'Info is shown below', 'data': data}, safe=False)


# shows all the tickets and the replies of that specific ticket
# This is for the admin
@api_view(['GET', ])
def ticket_list(request):

	try:
		tickets = Ticket.objects.all()
		ticketserializer = TicketSerializer(tickets, many=True)

		return JsonResponse(
			{
				'success': True,
				'message': 'Data has been retrieved successfully',
				'data': ticketserializer.data
			}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'There are no tickets'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', ])
def unattended_ticket_list(request):

	ticket_count = 0

	try:
		tickets = Ticket.objects.filter(is_attended=False)

	except:
		tickets = None

	if tickets:

		ticket_lists = list(tickets.values_list('id', flat=True).distinct())

		ticket_count = len(ticket_lists)

		ticketserializer = TicketSerializer(tickets, many=True)
		return JsonResponse(
			{
				'success': True,
				'message': 'Data has been retrieved successfully',
				'ticket_count': ticket_count,
				'data': ticketserializer.data
			}, safe=False)

	else:

		return JsonResponse(
			{
				'success': False,
				'message': 'No data is available',
				'ticket_count': ticket_count,
				'data': {}
			}, safe=False)


# Shows the ticket by a specific id and its replies
@api_view(['GET', ])
def specific_ticket(request, ticket_id):

	try:
		tickets = Ticket.objects.filter(id=ticket_id)
		ticketid = tickets.values_list('id', flat=True)
		replies = []
		for i in range(len(ticketid)):
			ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
			replies += ticketreplies
		ticketserializer = TicketSerializer(tickets, many=True)
		return JsonResponse({
			'success': True,
			'message': 'data has been retrived successfully',
			'data': ticketserializer.data
		}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'The ticket does not exist'
			}, status=status.HTTP_404_NOT_FOUND)


# Shows all the active tickets
@api_view(['GET', ])
def active_ticket(request):

	try:
		tickets = Ticket.objects.filter(is_active=True)
		ticketid = tickets.values_list('id', flat=True)
		replies = []
		for i in range(len(ticketid)):
			ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
			replies += ticketreplies

		ticketserializer = TicketSerializer(tickets, many=True)
		ticket_data = ticketserializer.data
		return JsonResponse({
			'success': True,
			'message': "Data has been retrived successfully",
			'data': ticket_data
		}, safe=False)

	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'The ticket does not exist'
			}, status=status.HTTP_404_NOT_FOUND)


# Shows all the tickets of a specific user
@api_view(['GET', ])
def sender_ticket(request, sender_id):

	try:
		tickets = Ticket.objects.filter(sender_id=sender_id)
		# ticketid = tickets.values_list('id' , flat = True)
		# replies = []
		# for i in range(len(ticketid)):
		# 	ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
		# 	replies += ticketreplies

	except:

		tickets = None

	if tickets:

		ticketserializer = TicketSerializer(tickets, many=True)
		# ticketrepliesserializer = TicketRepliesSerializer(replies,many=True)
		return JsonResponse({
			'success': True,
			'message': "data has been retrived successfully",
			'data': ticketserializer.data
		}, safe=False)

	else:

		return JsonResponse({
			'success': False,
			'message': 'The user does not have any tickets'
			})


# Shows all the tickets handled by a specific receiver
@api_view(['GET', ])
def receiver_ticket(request, receiver_id):

	user = User.objects.filter(id=receiver_id)
	if user.exists():
		try:
			tickets = Ticket.objects.filter(receiver_id=receiver_id)
			ticketid = tickets.values_list('id', flat=True)
			replies = []
			for i in range(len(ticketid)):
				ticketreplies = TicketReplies.objects.filter(ticket_id=ticketid[i])
				replies += ticketreplies

			ticketserializer = TicketSerializer(tickets, many=True)
			ticketrepliesserializer = TicketRepliesSerializer(replies, many=True)
			return JsonResponse({
				'success': True,
				'message': 'data has been retrived successfully',
				'data': ticketrepliesserializer.data
			}, safe=False)

		except Ticket.DoesNotExist:
			return JsonResponse({
				'success': False,
				'message': 'The ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)
	else:
		return JsonResponse({
				'success': False,
				'message': 'There is no ticket for this receiver'}, status=status.HTTP_404_NOT_FOUND)

# This creates a ticket


@api_view(['POST', ])
def create_ticket(request):
	ticket_serializer = TicketSerializer(data=request.data)
	if ticket_serializer.is_valid():
		ticket_serializer.save()
		return JsonResponse({
			'success': True,
			'message': 'Data has been retrieved successfully',
			'data': ticket_serializer.data
		}, status=status.HTTP_201_CREATED)
	return JsonResponse({
		'success': False,
		'message': 'Ticket could not be created',
		'error': ticket_serializer.errors
	})

# This updates a ticket info. The admin or support can add the receiver info and the department


@api_view(['POST', ])
def edit_ticketinfo(request, ticket_id):

	try:
		comment = Ticket.objects.get(id=ticket_id)
		if request.method == 'POST':
			commentserializer = TicketSerializer(comment, data=request.data)
			if commentserializer.is_valid():
				commentserializer.save()
				return JsonResponse({
					'success': True,
					'message': 'Information has been updated successfully',
					'data': commentserializer.data
				})
			return JsonResponse({
				'success': False,
				'message': 'Information could not be updated',
				'error': commentserializer.errors
			})
	except Ticket.DoesNotExist:
		return JsonResponse({
			'success': False,
			'message': 'This ticket does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', ])
# Creates a reply for a specific ticket reply
def create_reply(request, ticket_id):

	reply_name = ""
	staff = False

	user_id = request.data.get('user_id')

	try:

		names = User.objects.get(id=user_id)

	except:

		names = None

	if names:

		print("dhuksi")

		if names.username:

			reply_name = str(names.username)

		else:

			reply_name = ""

		staff = names.is_staff

		ticketreply = TicketReplies.objects.create(
		    ticket_id=ticket_id, user_id=user_id, name=reply_name, is_staff=staff)
		ticketreplies_serializer = TicketRepliesSerializer(
		    ticketreply, data=request.data)
		if ticketreplies_serializer.is_valid():
			ticketreplies_serializer.save()
			return JsonResponse({
			'success': True,
			'message': 'Reply has been created successfully',
			'data': ticketreplies_serializer.data
				}, status=status.HTTP_201_CREATED)

		else:

			return JsonResponse({
			'success': False,
			'message': 'Reply could not be vreated',
			'data': {}
				})

	else:

		return JsonResponse({
			'success': False,
			'message': 'Reply could not be vreated',
			'data': {}
				})


@api_view(['POST', ])
def edit_ticketreply(request, reply_id):

	comm = TicketReplies.objects.filter(pk=reply_id)
	if comm.exists():
		try:
			comment = TicketReplies.objects.get(pk=reply_id)
			if request.method == 'POST':
				commentserializer = TicketRepliesSerializer(comment, data=request.data)
				if commentserializer.is_valid():
					commentserializer.save()
					return JsonResponse({
						'success': True,
						'message': 'Reply has been updated successfully',
						'data': commentserializer.data
					})
				return JsonResponse({
					'success': False,
					'message': 'Problem while updating reply',
					'error': commentserializer.errors
				}, status=status.HTTP_400_BAD_REQUEST)

		except Ticket.DoesNotExist:
			return JsonResponse({
				'success': False,
				'message': 'This ticket reply does not exist'}, status=status.HTTP_404_NOT_FOUND)
	else:
		return JsonResponse({
				'success': False,
				'message': 'Invalid reply id'}, status=status.HTTP_404_NOT_FOUND)


# Delete a certain ticket
@api_view(['POST', ])
def delete_ticket(request, ticket_id):

	tickets = Ticket.objects.filter(pk=ticket_id)
	ticketreplies = TicketReplies.objects.filter(ticket_id=ticket_id)
	if request.method == 'POST':
		if tickets.exists():
			tickets.delete()
			ticketreplies.delete()
			return JsonResponse({
				'success': True,
				'message': 'Ticket was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
		else:

			return JsonResponse({
				'success': False,
				'message': 'Could not be deleted'
				})


@api_view(["GET", "POST"])
def insert_area(request):

    if request.method == 'POST':
        try:
            area_value = AreaSerializer(data=request.data)
            if(area_value.is_valid()):
                area_value.save()
                return Response({
                    'success': True,
                    'message': 'Data has been inserted successfully',
                    'data': area_value.data
                    }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'message': 'Data could not record',
                'error': area_value.errors
                })
        except:
            return Response({
                'success': False,
                'message': 'It occurs some problem to insert values',
                })


@api_view(["GET", "POST"])
def insert_location(request):

    if request.method == 'POST':
        try:
            location_value = LocationSerializer(data=request.data)
            if(location_value.is_valid()):
                location_value.save()
                return Response({
                    'success': True,
                    'message': 'Data has been inserted successfully',
                    'data': location_value.data
                    }, status=status.HTTP_201_CREATED)
            return Response({
                'success': False,
                'message': 'Data could not record',
                'error': location_value.errors
                })
        except:
            return Response({
                'success': False,
                'message': 'It occurs some problem to insert values',
                })


@api_view(["GET", "POST"])
def insert_delivery_charge(request):
	data_values = request.data
	area_id = -1
	location_id = -1

	if request.method == 'POST':
		area_values = {
			'specification_id': data_values['specification_id'],
			'Area_name': data_values['Area_name'],
			'Area_details': data_values['Area_details'],
		}

		location_values = {
			'location_name': data_values['location_name']
		}

		delivery_charge_values = {
			'height': data_values['height'],
			'width': data_values['width'],
			'length': data_values['length'],
			'weight': data_values['weight'],
			'measument_unit': data_values['measument_unit'],
			'unit_price': data_values['unit_price'],
			'delivery_day': data_values['delivery_day'],
			'minimum_amount': data_values['minimum_amount'],
		}
		try:

			all_area_list = DeliveryArea.objects.values_list(
				'Area_name', flat=True)
			if data_values['Area_name'] not in all_area_list:
				area_value = AreaSerializer(data=area_values)
				if(area_value.is_valid()):
					area_value.save()
					area_id = area_value.data['id']
					location_values.update({'area_id': area_value.data['id']})
			else:
				area_id_value = DeliveryArea.objects.filter(
					Area_name=data_values['Area_name'])
				area_id = area_id_value[0].id
				location_values.update({'area_id': area_id_value[0].id})

			all_location_list = DeliveryLocation.objects.filter(
				area_id=area_id, location_name=data_values['location_name'])
			if all_location_list.exists():
				location_id = all_location_list[0].id
				delivery_charge_values.update({'location_id': location_id})

			else:
				location_data = LocationSerializer(data=location_values)
				if(location_data.is_valid()):
					location_data.save()
					location_id = location_data.data['id']
					delivery_charge_values.update({'location_id': location_id})

			delivery_data = DeliverySerializer(data=delivery_charge_values)

			if(delivery_data.is_valid()):
				delivery_data.save()
				return Response({
					'success': True,
					'message': 'Data has been inserted successfully',
					}, status=status.HTTP_201_CREATED)
			return Response({
				'success': False,
				'message': 'Data could not record',
				})
		except:
			if location_id != -1:
				charge_value = DeliveryInfo.objects.filter(
					location_id=location_id)
				charge_value.delete()
			if area_id != -1:
				location_value = DeliveryLocation.objects.filter(
					area_id=area_id)
				area_value = DeliveryArea.objects.filter(id=area_id)
				area_value.delete()
				location_value.delete()
			return Response({
				'success': False,
				'message': 'It occurs some problem to insert values',
				})


@api_view(["GET", "POST"])
def get_all_areaz(request):

    try:
        area_value = DeliveryArea.objects.filter(is_active=True)
    except:
        return Response({
            'success': False,
            'message': 'It occurs some problem',
            })

    if request.method == 'GET':
        area_serializer_value = AreaSerializer(area_value, many=True)
        return Response(
            {
                'success': True,
                'message': 'Value has been retrieved successfully.',
                'data': area_serializer_value.data
            })


@api_view(["GET", ])
def get_all_areas(request,order_id):

	area_data = []
	area_ids = []
	print(order_id)

	try:
		items = OrderDetails.objects.filter(order_id = order_id,is_removed=False,delivery_removed=False)
	except:
		items = None 

	print(items)

	if items:
		item_ids = list(items.values_list('specification_id', flat=True))
		for i in range(len(item_ids)):
			try:
				product_delivery =  product_delivery_area.objects.filter(specification_id = item_ids[i])
				
			except:
				product_delivery = None 

			print("product_delivery_area")
			print(product_delivery)

			if product_delivery:

				product_delivery_infos =  list(product_delivery.values_list('is_Bangladesh', flat=True))
				print(product_delivery_infos)

				if True in product_delivery_infos:
					#return all the areas
					print("return all the areas")
					try:
						area_value = DeliveryArea.objects.all()

					except:
						area_value = None 

					if area_value:
						area_serializer_value = AreaSerializer(area_value, many=True)
						area_data = area_serializer_value.data
						return JsonResponse({"success":True,"message":"Data is shown","data":area_data})

		
		try:
			delivery_areas = product_delivery_area.objects.filter(specification_id__in = item_ids)

		except:
			delivery_areas = None 

		print("second phase")
		print(delivery_areas)

		if delivery_areas:
			delivery_area_ids = list(delivery_areas.values_list('delivery_area_id', flat=True).distinct())


		else:
			delivery_area_ids = []

		try:
			deli_areas = DeliveryArea.objects.filter(id__in = delivery_area_ids,is_active=True)
		except:
			deli_areas = None

		if deli_areas:
			area_serializer_value = AreaSerializer(deli_areas, many=True)
			area_data = area_serializer_value.data
			return JsonResponse({"success":True,"message":"Data is shown","data":area_data})

		else:
			return JsonResponse({"success": False,"message":"Data does not exist"})


	else:
		return JsonResponse({"success": False,"message":"Data is not shown"})


				

					


				





	#list(delivered_orders.values_list('id', flat=True))

    # try:
    #     area_value = DeliveryArea.objects.all()
    # except:
    #     return Response({
    #         'success': False,
    #         'message': 'It occurs some problem',
    #         })

    # if request.method == 'GET':
    #     area_serializer_value = AreaSerializer(area_value, many=True)
    #     return Response(
    #         {
    #             'success': True,
    #             'message': 'Value has been retrieved successfully.',
    #             'data': area_serializer_value.data
    #         })


# @api_view(["GET", "POST"])
# def get_specific_location(request, area_id):

#     try:
#         location_value = DeliveryLocation.objects.filter(area_id=area_id)
#     except:
#         return Response({
#             'success': False,
#             'message': 'It occurs some problem',
#             })

#     if request.method == 'GET':
#         location_serializer_value = LocationSerializer(
#             location_value, many=True)
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': location_serializer_value.data

#             })


# @api_view(["GET", "POST"])
# def get_specific_location(request, area_id):

#     try:
#         location_value = DeliveryLocation.objects.filter(area_id=area_id)
#     except:
#         return Response({
#             'success': False,
#             'message': 'It occurs some problem',
#             })

#     if request.method == 'GET':
#         location_serializer_value = LocationSerializer(
#             location_value, many=True)
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': location_serializer_value.data

#             })


# @api_view(["GET", "POST"])
# def get_estimated_value(request, area_name, location_name):
#     # data_values = {
#     #               "id": 27,
#     #               "date_created": "2020-11-04T11:49:31.364345+06:00",
#     #               "order_status": "Unpaid",
#     #               "delivery_status": "To ship",
#     #               "orders": [
#     #                   {
#     #                       "id": 65,
#     #                       "order_id": 27,
#     #                       "product_id": 64,
#     #                       "specification_id": 2,
#     #                   },
#     #                   {
#     #                       "id": 66,
#     #                       "order_id": 27,
#     #                       "product_id": 64,
#     #                       "specification_id": 3,
#     #                   },
#     #                   {
#     #                       "id": 67,
#     #                       "order_id": 27,
#     #                       "product_id": 64,
#     #                       "specification_id": 6,
#     #                   }
#     #               ]
#     #           }

#     data_values = request.data
#     if request.method == 'GET':
#         all_orders = data_values['orders']
#         total_price = 0
#         try:
#             area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
#             area_id = area_id_value[0].id
#             location_value = DeliveryLocation.objects.filter(area_id=area_id)
#             location_id = location_value[0].id
#             unit_price_value = DeliveryInfo.objects.filter(
#                 location_id=location_id).last()
#             unit_price = unit_price_value.unit_price
#             minimum_amount = unit_price_value.minimum_amount
#             delivery_day = unit_price_value.delivery_day
#         except:
#             return Response({
#                 'success': False,
#                 'message': 'It occurs some problem',
#             })

#         for order in all_orders:
#             spec_id = order['specification_id']
#             try:
#                 charge_value = DeliveryInfo.objects.get(
#                     specification_id=spec_id)
#             except:
#                 charge_value = None

#             if charge_value is not None:
#                 weight = charge_value.weight
#                 length = charge_value.length
#                 width = charge_value.width
#                 height = charge_value.height
#                 if weight > 0:
#                     price = weight*unit_price
#                     total_price = total_price + price
#                 elif ((length > 0) and (width > 0) and (height > 0)):
#                     weight = (length*width*height)/5000
#                     price = weight*unit_price
#                     total_price = total_price + price

#             else:
#                 return Response({
#                     'success': False,
#                     'message': 'It occurs some problem',
#                 })

#         if total_price < minimum_amount:
#             total_price = minimum_amount

#         data_values = {}
#         data_values.update({'estimated_price': total_price,
#                            'delivery_day': delivery_day})
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': data_values

#             })


@api_view(['POST', ])
def delete_estimation(request, area_id):
    if request.method == 'POST':
        area_data = DeliveryArea.objects.filter(id=area_id)
        location_data = DeliveryLocation.objects.filter(area_id=area_id)
        location_id = location_data[0].id
        delivery_value = DeliveryInfo.objects.filter(location_id=location_id)

        if area_data.exists():
            area_data.delete()
            location_data.delete()
            delivery_value.delete()
            return JsonResponse({
                'success': True,
                'message': 'Value is deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:

            return JsonResponse({
                'success': False,
                'message': 'Could not be deleted'
                })


# @api_view(["GET", "POST"])
# def getall_info_data(request):
#     areas = []
#     try:
#         area_value = DeliveryArea.objects.all()
#     except:
#         return Response({
#             'success': False,
#             'message': 'It occurs some problem',
#             })


#     if request.method == 'GET':
#         for area in area_value:
#             area_id = area.id
#             try:
#                 location_value = DeliveryLocation.objects.filter(area_id= area_id)
#             except:
#                 location_value= None
#             if location_value:
#                 datas={}
#                 insidecity ={}
#                 outsidecity={}
#                 for location in location_value:
#                     location_id = location.id
                    
#                     if ((location.location_name == 'inside City') or (location.location_name == 'Inside City')):
                        
#                         try:
#                             delivery_value = DeliveryInfo.objects.get(location_id=location_id)
#                         except:
#                             delivery_value= None
                        
#                         if delivery_value is not None:
#                             insidecity.update({'location_name':location.location_name, 'unit_price': delivery_value.unit_price, 'delivery_day': delivery_value.delivery_day, 'minimum_amount': delivery_value.minimum_amount})
#                             datas.update({'inside_city': insidecity })
#                     else:
#                         try:
#                             delivery_value = DeliveryInfo.objects.get(location_id=location_id)
#                         except:
#                             delivery_value= None
                        
#                         if delivery_value is not None:
#                             outsidecity.update({'location_name':location.location_name, 'unit_price': delivery_value.unit_price, 'delivery_day': delivery_value.delivery_day, 'minimum_amount': delivery_value.minimum_amount})
#                             datas.update({'outside_city': outsidecity })
#                 # val =  datas.keys()
#                 # if 'inside_city' not in val:
#                 #     datas.update({'inside_city': {}})
#                 # if 'outside_city' not in val:
#                 #     datas.update({'outside_city': {}})

#                 datas.update({'area_name': area.Area_name })
#                 areas.append(datas)
#             else:
#                 datas.update({'area_name': area.Area_name,'insidecity': {}, 'outsidecity': {}})
#                 areas.append(datas)
            

#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': areas
                
#             })


# @api_view(["GET", "POST"])
# def getall_info_data(request):
#     areas = []
#     try:
#         area_value = DeliveryArea.objects.all()
#     except:
#         return Response({
#             'success': False,
#             'message': 'It occurs some problem',
#             })
#     if request.method == 'GET':
#         for area in area_value:
#             area_id = area.id
#             try:
#                 location_value = DeliveryLocation.objects.filter(area_id= area_id)
#             except:
#                 location_value= None
#             if location_value:
#                 datas={}
#                 insidecity ={}
#                 outsidecity={}
#                 for location in location_value:
#                     location_id = location.id
                    
#                     if ((location.location_name == 'inside City') or (location.location_name == 'Inside City')):
                        
#                         try:
#                             delivery_value = DeliveryInfo.objects.filter(location_id=location_id).last()
#                         except:
#                             delivery_value= None
                        
#                         if delivery_value is not None:
#                             insidecity.update({'location_name':location.location_name, 'unit_price': delivery_value.unit_price, 'delivery_day': delivery_value.delivery_day, 'minimum_amount': delivery_value.minimum_amount})
#                             datas.update({'inside_city': insidecity })
#                     else:
#                         try:
#                             delivery_value = DeliveryInfo.objects.filter(location_id=location_id).last()
#                         except:
#                             delivery_value= None
                        
#                         if delivery_value is not None:
#                             outsidecity.update({'location_name':location.location_name, 'unit_price': delivery_value.unit_price, 'delivery_day': delivery_value.delivery_day, 'minimum_amount': delivery_value.minimum_amount})
#                             datas.update({'outside_city': outsidecity })
#                 val =  datas.keys()
#                 if 'inside_city' not in val:
#                     datas.update({'inside_city': {}})
#                 if 'outside_city' not in val:
#                     datas.update({'outside_city': {}})

#                 datas.update({'area_name': area.Area_name })
#                 areas.append(datas)
#             else:
#                 datas.update({'area_name': area.Area_name,'insidecity': {}, 'outsidecity': {}})
#                 areas.append(datas)
            

#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': areas
                
#             })



@api_view(["GET", "POST"])
def getall_info_data(request):
	if request.method == 'GET':
		try:
			areas = []
			area_value = DeliveryArea.objects.all()
			for area in area_value:
				district ={}
				thanas=[]
				thana_values = DeliveryLocation.objects.filter(area_id = area.id)
				for thana in thana_values:
					thana_name={}
					thana_data = DeliveryInfo.objects.filter(location_id = thana.id)
					if thana_data.exists():
						n = len(thana_data)-1
						delivery_data = DeliverySerializer (thana_data[n], many= False)
						delivery_val = delivery_data.data
						thanas.append(delivery_val)
				district.update({'district_name': area.Area_name, 'thanas':thanas})
				areas.append(district)
			return Response(
				{
					'success': True,
					'message': 'Value has been retrieved successfully.',
					'data': areas
					
				})
		except:
			return Response(
				{
					'success': False,
					'message': 'Something went wrong !!'
					
				})
        # for area in area_value:
        #     area_id = area.id
        #     try:
        #         location_value = DeliveryLocation.objects.filter(area_id= area_id)
        #     except:
        #         location_value= None
        #     if location_value:
        #         datas={}
        #         insidecity ={}
        #         outsidecity={}
        #         for location in location_value:
        #             location_id = location.id
                    
        #             if ((location.location_name == 'inside City') or (location.location_name == 'Inside City')):
                        
        #                 try:
        #                     delivery_value = DeliveryInfo.objects.filter(location_id=location_id).last()
        #                 except:
        #                     delivery_value= None
                        
        #                 if delivery_value is not None:
        #                     insidecity.update({'location_name':location.location_name, 'unit_price': delivery_value.unit_price, 'delivery_day': delivery_value.delivery_day, 'minimum_amount': delivery_value.minimum_amount})
        #                     datas.update({'inside_city': insidecity })
        #             else:
        #                 try:
        #                     delivery_value = DeliveryInfo.objects.filter(location_id=location_id).last()
        #                 except:
        #                     delivery_value= None
                        
        #                 if delivery_value is not None:
        #                     outsidecity.update({'location_name':location.location_name, 'unit_price': delivery_value.unit_price, 'delivery_day': delivery_value.delivery_day, 'minimum_amount': delivery_value.minimum_amount})
        #                     datas.update({'outside_city': outsidecity })
        #         val =  datas.keys()
        #         if 'inside_city' not in val:
        #             datas.update({'inside_city': {}})
        #         if 'outside_city' not in val:
        #             datas.update({'outside_city': {}})

        #         datas.update({'area_name': area.Area_name })
        #         areas.append(datas)
        #     else:
        #         datas.update({'area_name': area.Area_name,'insidecity': {}, 'outsidecity': {}})
        #         areas.append(datas)
            

        


# Shows check runner api enable or disable
@api_view(['GET',])
def enable_checking(request, api_name):

    try:

        api_value = APIs.objects.filter(name = api_name)
        if api_value:

        	# print("dhuktesse")
            enable_res = api_value[0].is_enable
            if enable_res is True:
                return JsonResponse({
                    'success': True,
                    'message': 'Value has been retrieved successfully',
                    'status': 'enabled'
                }, safe=False)
            else:
                return JsonResponse({
                    'success': True,
                    'message': 'Value has been retrieved successfully',
                    'status': 'disabled'
                }, safe=False)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Value does not'
            })
                
    except:
        return JsonResponse({
            'success': False,
            'message': 'Value does not exists'
            })





@api_view(['GET', 'POST'])
def make_enable_disable(request,name,status):
    # status 0, make disable
    try:
        api_value = APIs.objects.get(name = name)
    except:
        api_value = None
    
    try:
        if api_value is not None:
            if status == 0:
                serializer_data = ApienabledisableSerializer (api_value, data= {'is_enable': False})
                if serializer_data.is_valid():
                    serializer_data.save()
                    return JsonResponse({
                        'success': True,
                        'message': 'API successfully Disabled'
                    })
            # status 1, make anable
            if status == 1:
                if api_value.API_key == request.data['API_key']:
                    serializer_data = ApienabledisableSerializer (api_value, data= {'is_enable': True, 'area_url': request.data['area_url'],'location_url': request.data['location_url'],'estimation_url': request.data['estimation_url']})
                    if serializer_data.is_valid():
                        serializer_data.save()
                        return JsonResponse({
                            'success': True,
                            'message': 'API successfully Enabled'
                        })
                else:
                    return JsonResponse({
                            'success': False,
                            'message': 'Invalid API credentials !!'
                    })

        else:
            return JsonResponse({
                    'success': False,
                    'message': 'API with this name does not exists !!'
            })

    except:
        return JsonResponse({
                    'success': False,
                    'message': 'Something went wrong !!'
            })



# @api_view(['GET',])
# def get_all_active_delivery_base_url(request):

#     if request.method == 'GET':
#         try:
#             deliver_base_url = ""
#             delivery_api= APIs.objects.filter(Q(API_type= 'Delivery', is_enable = True) | Q(API_type= 'delivery',is_enable = True))
#             if delivery_api.exists():
#                 value = delivery_api[0]
#                 deliver_base_url = value.base_url
#             else:
#                 current_site = Site.objects.get_current()
#                 site_val = current_site.domain
#                 deliver_base_url= site_val
#             return JsonResponse({
#                     'success': True,
#                     'message': 'Valus has been retrieved successfully !!',
#                     'Base_url': deliver_base_url
#             })
#         except:
#             return JsonResponse({
#                     'success': False,
#                     'message': 'Something went wrong !!'
#             })


@api_view(['GET', 'POST'])
def get_all_active_delivery_base_url(request):

    if request.method == 'GET':
        try:
            datas= {}
            deliver_area_url = ""
            deliver_location_url = ""
            deliver_estimation_url = ""
            delivery_api= APIs.objects.filter(Q(API_type= 'Delivery', is_enable = True) | Q(API_type= 'delivery',is_enable = True))
            if delivery_api.exists():
                value = delivery_api[0]
                deliver_area_url = value.area_url
                deliver_location_url = value.location_url
                deliver_estimation_url = value.estimation_url
            else:
                current_site = Site.objects.get_current()
                site_val = current_site.domain
                deliver_base_url= site_val
                deliver_area_url = site_val+'/supports/allareas'
                deliver_location_url = site_val+'/supports/getlocation'
                deliver_estimation_url = site_val+'/supports/estimations'

            datas.update ({'area_url':deliver_area_url, 'location_url':deliver_location_url, 'estimation_url':deliver_estimation_url})
            return JsonResponse({
                    'success': True,
                    'message': 'Valus has been retrieved successfully !!',
                    'all_url': datas
            })
        except:
            return JsonResponse({
                    'success': False,
                    'message': 'Something went wrong !!'
            })



# @api_view(["GET", "POST"])
# def get_estimated_value(request,area_name,location_name):
#     # data_values = {
#     #                 "id": 27,
#     #                 "date_created": "2020-11-04T11:49:31.364345+06:00",
#     #                 "order_status": "Unpaid",
#     #                 "delivery_status": "To ship",
#     #                 "orders": [
#     #                     {
#     #                         "id": 65,
#     #                         "order_id": 27,
#     #                         "product_id": 64,
#     #                         "specification_id": 2,
#     #                     },
#     #                     {
#     #                         "id": 66,
#     #                         "order_id": 27,
#     #                         "product_id": 64,
#     #                         "specification_id": 3,
#     #                     }
                        
#     #                 ]
#     #             }

#     data_values= request.data
#     if request.method == 'POST':
#         all_orders = data_values['orders']
#         total_price = 0
#         try:
#             area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
#             area_id = area_id_value[0].id
#             location_value = DeliveryLocation.objects.filter(area_id=area_id)
#             location_id = location_value[0].id
#             unit_price_value= DeliveryInfo.objects.filter(location_id=location_id).last()
#             unit_price= unit_price_value.unit_price
#             minimum_amount = unit_price_value.minimum_amount
#             delivery_day = unit_price_value.delivery_day
#         except:
#             return Response({
#                 'success': False,
#                 'message': 'It occurs some problem',
#                 'data': []
#             })
            
#         for order in all_orders:
#             spec_id =  order['specification_id']
            
#             try:
#                 charge_value = DeliveryInfo.objects.get(specification_id=spec_id)
#             except:
#                 charge_value= None
#             if charge_value is not None:
#                 if charge_value.weight:
#                     weight = charge_value.weight
#                 else:
#                     weight= 0.0
#                 if charge_value.length:
#                     length = charge_value.length
#                 else:
#                     length = 0.0
#                 if charge_value.width:
#                     width = charge_value.width
#                 else:
#                     width = 0.0
#                 if charge_value.height:
#                     height = charge_value.height
#                 else:
#                     height = 0.0
#                 if weight>0:
#                     price = weight*unit_price
#                     total_price = total_price + price
#                 elif ((length>0) and (width>0) and (height>0)):
#                     weight = (length*width*height)/5000
#                     price = weight*unit_price
#                     total_price = total_price + price
        
#             else:
#                 return Response({
#                     'success': False,
#                     'message': 'It occurs some problem',
#                     'data': []
#                 })
        

#         if total_price < minimum_amount:
#             total_price = minimum_amount
        
#         data_values = {}
#         data_values.update({'price':total_price, 'days': delivery_day })
#         return Response (
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': [data_values]
                
#             })



# @api_view(["GET", "POST"])
# def get_specific_location(request, area_name):

#     try:
#         area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
#         area_id = area_id_value[0].id
#         location_value = DeliveryLocation.objects.filter(area_id=area_id)
#     except:
#         return Response({
#             'success': False,
#             'message': 'It occurs some problem',
#             })

#     if request.method == 'GET':
#         location_serializer_value = LocationSerializer(
#             location_value, many=True)
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': location_serializer_value.data

#             })



@api_view(["GET", "POST"])
def get_specific_location(request, area_name,order_id):

	all_flag = check_all_locations(order_id)

	if all_flag == True:

		try:
			area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
			area_id = area_id_value[0].id
			location_value = DeliveryLocation.objects.filter(area_id=area_id)
		except:
			return Response({
				'success': False,
				'message': 'It occurs some problem',
				})

		if request.method == 'GET':
			location_serializer_value = LocationSerializer(
				location_value, many=True)
			return Response(
				{
					'success': True,
					'message': 'Value has been retrieved successfully.',
					'data': location_serializer_value.data

				})

	else:
		specification_ids = get_specification_ids(order_id)
		location_ids = []
		try:
			area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
		except:
			area_id_value = None 

		if area_id_value:
			area_id = area_id_value[0].id

		else:
			area_id = 0 

		for j in range(len(specification_ids)):
			try:
				product_deli_area = product_delivery_area.objects.filter(specification_id=specification_ids[j],delivery_area_id=area_id).last()

			except:
				product_deli_area = None 

			if product_deli_area:
				loc_ids = product_deli_area.delivery_location_ids
				for m in range(len(loc_ids)):
					location_ids.append(loc_ids[m])

			else:
				pass

		location_ids = list(set(location_ids))

		try:
			locations = DeliveryLocation.objects.filter(id__in=location_ids)

		except:
			locations = None 

		if locations:
				location_serializers = LocationSerializer(locations,many=True)
				return JsonResponse({"success":True,"message":"The locations are shown","data":location_serializers.data})

		else:
			return JsonResponse({"success":False,"message":"No location exists"})

				




			
			








def get_specification_ids(order_id):

	specification_ids = []

	try:
		items = OrderDetails.objects.filter(order_id = order_id,is_removed=False,delivery_removed=False)
	except:
		items = None 

	print(items)

	if items:
		specification_ids = list(items.values_list('specification_id', flat=True))

	else:
		specification_ids = []


	return specification_ids





def check_all_locations(order_id):
	all_locations = False

	try:
		items = OrderDetails.objects.filter(order_id = order_id,is_removed=False,delivery_removed=False)
	except:
		items = None 

	print(items)

	if items:
		item_ids = list(items.values_list('specification_id', flat=True))
		for i in range(len(item_ids)):
			try:
				product_delivery =  product_delivery_area.objects.filter(specification_id = item_ids[i])
				
			except:
				product_delivery = None 

			print("product_delivery_area")
			print(product_delivery)

			if product_delivery:

				product_delivery_infos =  list(product_delivery.values_list('is_Bangladesh', flat=True))
				print(product_delivery_infos)

				if True in product_delivery_infos:
					#return all the areas
					return True
					#return JsonResponse({"success":True})
					# print("return all the areas")
					# try:
					# 	area_value = DeliveryArea.objects.all()

					# except:
					# 	area_value = None 

					# if area_value:
					# 	area_serializer_value = AreaSerializer(area_value, many=True)
					# 	area_data = area_serializer_value.data
					# 	return JsonResponse({"success":True,"message":"Data is shown","data":area_data})

				else:
					pass

		#return JsonResponse({"success": False})
		return False 

	else:
		#return JsonResponse({"success":False})
		return False

		





# @api_view(["GET", "POST"])
# def get_specific_location(request, area_name,order_id):

#     try:
#         area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
#         area_id = area_id_value[0].id
#         location_value = DeliveryLocation.objects.filter(area_id=area_id)
#     except:
#         return Response({
#             'success': False,
#             'message': 'It occurs some problem',
#             })

#     if request.method == 'GET':
#         location_serializer_value = LocationSerializer(
#             location_value, many=True)
#         return Response(
#             {
#                 'success': True,
#                 'message': 'Value has been retrieved successfully.',
#                 'data': location_serializer_value.data

#             })


def all_free(data):

	data_values = data


	all_orders = data_values['orders']
	delivery_infos = []
	for i in range(len(all_orders)):
		specification_id = all_orders[i]["specification_id"]
		try:
			delivery_info = DeliveryInfo.objects.filter(specification_id=specification_id).last()

		except:
			delivery_info = None 

		if delivery_info:
			flag = delivery_info.delivery_free
			delivery_infos.append(flag)

	print(delivery_infos)

	if False in delivery_infos:
		# return JsonResponse({"success":False}) 
		return False

	else:
		return True

@api_view(["GET",])
def get_specific_locationz(request, area_name):

    try:
        area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
        area_id = area_id_value[0].id
        location_value = DeliveryLocation.objects.filter(area_id=area_id)
    except:
        return Response({
            'success': False,
            'message': 'It occurs some problem',
            })

    if request.method == 'GET':
        location_serializer_value = LocationSerializer(
            location_value, many=True)
        return Response(
            {
                'success': True,
                'message': 'Value has been retrieved successfully.',
                'data': location_serializer_value.data

            })
	


@api_view(["GET", "POST"])
def get_estimated_value(request,area_name,location_name):
    # data_values = {
    #                 "id": 27,
    #                 "date_created": "2020-11-04T11:49:31.364345+06:00",
    #                 "order_status": "Unpaid",
    #                 "delivery_status": "To ship",
    #                 "orders": [
    #                     {
    #                         "id": 65,
    #                         "order_id": 27,
    #                         "product_id": 64,
    #                         "specification_id": 2,
    #                     },
    #                     {
    #                         "id": 66,
    #                         "order_id": 27,
    #                         "product_id": 64,
    #                         "specification_id": 3,
    #                     }
    #                 ]
    #             }
	data_values= request.data
	# data_values = {
	# 				"id": 27,
	# 				"date_created": "2020-11-04T11:49:31.364345+06:00",
	# 				"order_status": "Unpaid",
	# 				"delivery_status": "To ship",
	# 				"orders": [
	# 							{
	# 								"id": 65,
	# 								"order_id": 27,
	# 								"product_id": 64,
	# 								"specification_id": 2,
	# 							},
	# 							{
	# 								"id": 66,
	# 								"order_id": 27,
	# 								"product_id": 64,
	# 								"specification_id": 3,
	# 							}
	# 						]
	# 				}		
	if request.method == 'POST':
		print("method ey dhukar aage")

		all_flag = all_free(data_values)
		# if all_flag == True
		print("all_flag")
		print(all_flag)

		if all_flag == True:

			print("shob False")

			try:
				all_orders = data_values['orders']
				total_price = 0
				location_id = -1
				try:
					area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
					print("area_id_value")
					print(area_id_value)
					area_id = area_id_value[0].id
					location_value = DeliveryLocation.objects.filter(area_id=area_id)
					print(location_value)
					for locations in location_value:
						print(locations.location_name)
						if locations.location_name == location_name:
							location_id = locations.id

					print(location_id)
					unit_price_value= DeliveryInfo.objects.filter(location_id=location_id).last()
					print(unit_price_value)
					unit_price= unit_price_value.unit_price
					print(unit_price)
					minimum_amount = unit_price_value.minimum_amount
					print(minimum_amount)
					delivery_day = unit_price_value.delivery_day
					print(delivery_day)
				except:
					print("cndwfhwdufhnufbn")
					return Response({
						'success': False,
						'message': 'It occurs some problem',
					})
				for order in all_orders:
					spec_id =  order['specification_id']
					print("specification")
					print(spec_id)
					try:
						charge_value = DeliveryInfo.objects.filter(specification_id=spec_id)
					except:
						charge_value= None

					print("charge_value")
					print(charge_value)
					if charge_value is not None:
						# if charge_value[0].measument_unit == "gm":
						# 	weight 


						if charge_value[0].weight:
							weight = charge_value[0].weight
						else:
							weight= 0.0

						if charge_value[0].measument_unit:
							if charge_value[0].measument_unit == "gm":
								weight = weight/1000
							else:
								weight = weight

						print("WEIGHT")
						print(weight)
						if charge_value[0].length:
							length = charge_value[0].length
						else:
							length = 0.0
						if charge_value[0].width:
							width = charge_value[0].width
						else:
							width = 0.0
						if charge_value[0].height:
							height = charge_value[0].height
						else:
							height = 0.0
						if weight>0:
							price = weight*unit_price
							total_price = total_price + price
						elif ((length>0) and (width>0) and (height>0)):
							weight = (length*width*height)/5000
							price = weight*unit_price
							total_price = total_price + price
					else:
						print("xxxxxx")
						return Response({
							'success': False,
							'message': 'It occurs some problem',
						})
				if total_price < minimum_amount:
					total_price = minimum_amount
				data_values = {}
				data_values.update({'price': 0, 'days': delivery_day })
				return Response (
					{
						'success': True,
						'message': 'Value has been retrieved successfully.',
						'data': [data_values]
					})

			except:
				return Response (
					{
						'success': False,
						'message': 'Something went wrong !!'
					})

		else:

			try:
				all_orders = data_values['orders']
				total_price = 0
				location_id = -1
				try:
					area_id_value = DeliveryArea.objects.filter(Area_name=area_name)
					print("area_id_value")
					print(area_id_value)
					area_id = area_id_value[0].id
					location_value = DeliveryLocation.objects.filter(area_id=area_id)
					print(location_value)
					for locations in location_value:
						print(locations.location_name)
						if locations.location_name == location_name:
							location_id = locations.id

					print(location_id)
					unit_price_value= DeliveryInfo.objects.filter(location_id=location_id).last()
					print(unit_price_value)
					unit_price= unit_price_value.unit_price
					print(unit_price)
					minimum_amount = unit_price_value.minimum_amount
					print(minimum_amount)
					delivery_day = unit_price_value.delivery_day
					print(delivery_day)
				except:
					print("cndwfhwdufhnufbn")
					return Response({
						'success': False,
						'message': 'It occurs some problem',
					})
				for order in all_orders:
					spec_id =  order['specification_id']
					print("specification")
					print(spec_id)
					try:
						charge_value = DeliveryInfo.objects.filter(specification_id=spec_id)
					except:
						charge_value= None

					print("charge_value")
					print(charge_value)
					if charge_value is not None:
						# if charge_value[0].measument_unit == "gm":
						# 	weight 

						if charge_value[0].delivery_free:
							delivery_free = charge_value[0].delivery_free

						else:
							delivery_free = False

						print(delivery_free)

						if delivery_free == False:

							print("delivery false hochche")


							if charge_value[0].weight:
								weight = charge_value[0].weight
							else:
								weight= 0.0

							if charge_value[0].measument_unit:
								if charge_value[0].measument_unit == "gm":
									weight = weight/1000
								else:
									weight = weight

							print("WEIGHT")
							print(weight)
							if charge_value[0].length:
								length = charge_value[0].length
							else:
								length = 0.0
							if charge_value[0].width:
								width = charge_value[0].width
							else:
								width = 0.0
							if charge_value[0].height:
								height = charge_value[0].height
							else:
								height = 0.0
							if weight>0:
								
								price = weight*unit_price
								total_price = total_price + price
								print("total_price")
								print(total_price)
							elif ((length>0) and (width>0) and (height>0)):
								weight = (length*width*height)/5000
								price = weight*unit_price
								total_price = total_price + price
								print("total_price")
								print(total_price)

						else:
							price = 0 
							total_price = total_price + price

					else:
						print("xxxxxx")
						return Response({
							'success': False,
							'message': 'It occurs some problem',
						})
				if total_price < minimum_amount:
					total_price = minimum_amount
				data_values = {}
				data_values.update({'price':total_price, 'days': delivery_day })
				return Response (
					{
						'success': True,
						'message': 'Value has been retrieved successfully.',
						'data': [data_values]
					})

			except:
				return Response (
					{
						'success': False,
						'message': 'Something went wrong !!'
					})





@api_view(['GET', 'POST'])
def make_district_active_inactive(request,name,status):
	# status 0, make disable
	try:
		district_value = DeliveryArea.objects.get(Area_name = name)
	except:
		district_value = None
	try:
		if district_value is not None:
			# if status 0 then make inactive
			if status == 0:
				district_value.is_active = False
				district_value.save()
				return JsonResponse({
					'success': True,
					'message': 'District successfully Disabled'
				})
			# status 1, make enable
			if status == 1:
				district_value.is_active = True
				district_value.save()
				return JsonResponse({
					'success': True,
					'message': 'District successfully Enabled'
				})
		else:
			return JsonResponse({
					'success': False,
					'message': 'This District does not exists !!'
			})
	except:
		return JsonResponse({
					'success': False,
					'message': 'Something went wrong !!'
			})
@api_view(['GET', 'POST'])
def make_thanas_active_inactive(request,name,status):
	# status 0, make disable
	try:
		location_value = DeliveryLocation.objects.get(location_name = name)
	except:
		location_value = None
	try:
		if location_value is not None:
			# if status 0 then make inactive
			if status == 0:
				location_value.is_active = False
				location_value.save()
				return JsonResponse({
					'success': True,
					'message': 'Thana successfully Disabled'
				})
			# status 1, make enable
			if status == 1:
				location_value.is_active = True
				location_value.save()
				return JsonResponse({
					'success': True,
					'message': 'Thana successfully Enabled'
				})
		else:
			return JsonResponse({
					'success': False,
					'message': 'This Thana does not exists !!'
			})
	except:
		return JsonResponse({
					'success': False,
					'message': 'Something went wrong !!'
			})



@api_view(['POST',])
def product_change(request):

	try:
		products = Product.objects.all()
	except:
		products = None 

	if products:

		product_ids = list(products.values_list('id', flat=True))

		for i in range(len(product_ids)):

			try:
				in_product = Product.objects.get(id=product_ids[i])
			except:
				in_product = None 

			if in_product:
				in_product.lowest_spec_id = -1
				in_product.old_price = 0.00 
				in_product.new_price = 0.00 
				in_product.save()

			else:
				pass

		
		return JsonResponse({"message":"successful"})

	else:

		return JsonResponse({"message":"unsuccessful"})