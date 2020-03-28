import json

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from datetime         import datetime,timedelta,timezone
from django.db.models import Avg

from .models        import Review, TravelObject, Age
from product.models import TourProduct
from account.models import Account
from account.utils  import Login_Check

class ReviewView(View):
    @Login_Check
    def post(self, request):
        try:
            data       = json.loads(request.body)
            product_id = data['product_id']

            if TourProduct.objects.filter(id = product_id).exists():

                review = Review(
                    content         = data['content'],
                    rating          = data['rating'],
                    account_id      = request.user,
                    tour_product_id = product_id
                )
                review.save()

                return HttpResponse(status=200)
            return JsonResponse({'message' : 'INVALID_PRODUCT'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status=400)

    def get(self, request):
        product_id = request.GET.get('product_id' , None) 

        if not product_id:
            return JsonResponse({'message' : 'PRODUCT_ID_MISSING'}, status=400)

        review_list = [{
            'id'      : review_data.id,
            'name'    : review_data.account.username,
            'content' : review_data.content,
            'rating'  : review_data.rating,
            'date'    : review_data.created_at
            } for review_data in Review.objects.filter(tour_product_id = product_id)]

        return JsonResponse({'Review_list' : review_list}, status=200)


class ReviewDetail(View):
    @Login_Check
    def post(self, request, review_id):
        try:
            review    = Review.objects.filter(id = review_id, account_id = request.user)
            data      = json.loads(request.body)

            review.update(
                content = data['content'],
                rating  = data['rating']
            )

            return HttpResponse(status=200)

        except Review.DoesNotExist:
            return JsonResponse({'message' : 'UNAUTHORIZED'}, status=401)
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEYS'}, status=400)

    @Login_Check
    def delete(self, request, review_id): 
        try:        
            Review.objects.get(id = review_id, account_id = request.user).delete()

            return HttpResponse(status=200)
                    
        except Review.DoesNotExist:
            return JsonResponse({'error' : 'UNAUTHORIZED'}, status=401)
