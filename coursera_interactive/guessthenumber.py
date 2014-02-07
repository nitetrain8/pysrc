class myobject():
    
    def __init__(self):
        
        print("init")
    
    def commit(self):
        print("commit")
        
    def rollback(self):
        print("rollback")
        
    def close(self):
        del self




def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = myobject()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
        
a = session_scope()
i = a
print(list(a))   