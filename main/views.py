from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
class IsOwner(BasePermission):
    message = "you don't have the permission to access this object"

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email = email)
            if not user.check_password(password):
                return Response("password incorrect", status = status.HTTP_400_BAD_REQUEST)
            token = Token.objects.get(user = user)
            return Response({'token':token.key, 'user':UserSerializer(user).data}) 
        except User.DoesNotExist:
            return Response("user with this email not found", status = status.HTTP_404_NOT_FOUND)
        

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user = user)
            return Response({'token':token.key, 'user':serializer.data})
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class IncomeCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    # def perform_create(self, serializer):   ### it creates the object normally but still giving the user field is required error
    #     serializer.save(user = self.request.user)

class IncomeListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

    def get_queryset(self):
        user = self.request.user
        return Income.objects.filter(user = user).order_by('-date', '-id')

class IncomeDetailView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    lookup_field = 'id'

class IncomeUpdateView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    lookup_field = 'id'

    # def put(self, request, id):
    #     try:
    #         income = Income.objects.get(id=id, user=request.user)
    #     except Income.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     serializer = IncomeSerializer(income, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def patch(self, request, id):
    #     try:
    #         income = Income.objects.get(id=id, user=request.user)
    #     except Income.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     serializer = IncomeSerializer(income, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeDeleteView(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    lookup_field = 'id'

   

class ExpenseCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class ExpenseListView(ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        return Expense.objects.filter(user = user).order_by('-date', '-id')

class ExpenseDetailView(RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'id'

class ExpenseUpdateView(UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'id'

class ExpenseDeleteView(DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    lookup_field = 'id'

class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductListView(ListAPIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductCreateView(CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    



# class TransactionsList(APIView):
#     def get(self, request):
#         user = request.user
#         try:
#             transactions = Transaction.objects.filter(user = user)
#         except:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = TransactionSerializer(transactions, many = True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def post(self, request):
#         serializer = TransactionSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save() ## triggers the create method in the serializer
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


# class TransactionDetails(APIView):   
#     def get(self, request, id):
#         try:
#             transaction = Transaction.objects.get(pk = id)
#         except:
#             return Response(status = status.HTTP_404_NOT_FOUND)
        
#         if request.user != transaction.user:   #search if we can do this using DetailView with a decorator or something, or create a decorator.
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = TransactionSerializer(transaction)
#         return Response(serializer.data)

#     def delete(self, request, id):
#         try:
#             transaction = Transaction.objects.get(pk = id)
#         except:
#             return Response(status = status.HTTP_404_NOT_FOUND)

#         if request.user != transaction.user:
#             return Response("you don't have previllages to remove this", status=status.HTTP_403_FORBIDDEN)
        
#         transaction.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

#     def put(self, request, id):
#         try:
#             transaction = Transaction.objects.get(pk = id)
#         except:
#             return Response(status = status.HTTP_404_NOT_FOUND)

#         if request.user != transaction.user:
#             return Response("you don't have previllages to edit this", status=status.HTTP_403_FORBIDDEN)

#         serializer = TransactionSerializer(transaction, request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, id):
#         try:
#             transaction = Transaction.objects.get(pk = id)
#         except:
#             return Response(status = status.HTTP_404_NOT_FOUND)

#         if request.user != transaction.user:
#             return Response("you don't have previllages to edit this", status=status.HTTP_403_FORBIDDEN)

#         serializer = TransactionSerializer(transaction, request.data, partial = True)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class getAnalytics(APIView):
#     def get(self, request):
#         user = request.user
#         ##transactions per category
#         data = {
            
#         }
        
#         categories = Category.objects.all()
#         for category in categories:
#             transactions = Transaction.objects.filter(category = category, user = user)
#             total_amount = 0
#             for trans in transactions:
#                 total_amount += trans.amount
#             data[category].append(total_amount)


