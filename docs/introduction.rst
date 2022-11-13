Introduction
============

A Django library for managing user access using roles.
The built in Django permission system is great for fine grain user
access management, but it does not suit every use case.

Django RAM aims to solve the following problems by offering an alternative user
management system that revolves around roles:

1. Django permissions are tightly coupled to a specific model via a
   content type. This is not well suited for managing access to
   non-model resources or a collection of related records.
2. Integration with Django Rest Framework is cumbersome at best.
3. It can become difficult to keep track of user API access by looking
   at the source code, specifically with regards to DRF views and
   viewsets. Access to a DRF resource can easily become a complex and
   scattered function of DRF permission classes and user permission
   checks (permissions which may be inherited from any number of user
   groups.)

