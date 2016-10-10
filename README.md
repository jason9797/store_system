# store_system
a failed system. just give up!

Fuction:

  1.user module(app{role})
  
    (1).permission management
    (2).user CRUD operation
    (3).user role management
    (4).homepage(need some data through order),bind with user
    (5).sale goal,cut management
    (6).issuing_person management(issusing_person is a staff of sale)
  2.order module(app{order})
  
    (1).customer management
    (2).product management
    (3).order management
    #all management have CRUD operation
    (4).customer management include module(customer,customer_level,customer_alert,customerfile,contact_info)
    (5).product management include module(product only now)
    (6).order management include module(order,order_all_info,order_server,order_state,orderfile)
    (7).order userlog(trace customer ,order(CRUD operation,data save in postgresql hstore))
  3.stock module(app{stock})
  
    #not show in web,will add in next version
    
    
