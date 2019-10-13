#include <stdlib.h>
#include <assert.h>
struct SL_Base_;
struct SLNode_;

typedef struct SLBase_ SLBase;
typedef struct SLNode_ SLNode;

SL_Base* SingleLinkedList(void);

#define NODE_NOT_FOUND -1

#ifdef RUNSAFE 
#define findPrevNode(base, node) findPrevNodeSafe(base, node)
#else
#defien findPrevNode(base, node) findPrevNodeUnsafe(base, node)


#define SL_NODE_IS_HEAD(base, node) ((base->head == node))
#define SL_NODE_IS_TAIL(base, node) ((base->tail == node))
#define SL_NODE_IS_TAIL_OR_BASE(base, node) ((base->head==node) || (base->tail == node))

struct SLBase_ {
	SLNode* tail;
	SLNode* head;
};

struct SLNode_ {

	SLNode* next;
	void * data;
	
};


int main(int argc, char* argv[], char* env[]){



	return 0;
}

SLBase* newSingleLinkedList(void){

	SLBase * new = malloc(sizeof(struct SLBase_);
	new->tail = NULL;
	new->head = NULL;

	return new;
}

void dtorSLBase(struct SLBase_ ** pbase){
     /*naively destroy entire list through iteration*/
	 
	 /* Casting SLNode to SLBase will allow this function
	 to destruct SLNode as well */
	 
	 struct SL_Base_ * base = *pbase;
	 
	 SLNode * ptail = base->tail;
	 SLNode * pnext;
	 
	 if(ptail == NULL){
		return;
	 }

	do {
		 pnext = ptail->next; //either next node or NULL
		 free(ptail);
		 ptail = pnext; // if NULL, both pointers are now NULL
	} while (pnext != NULL);
	
	free(base);
	*pbase = NULL;
	
}

int delSLNode(const struct SLBase_ * base, SLNode ** node){

	SLNode * pnext = node->next;
	
	if (SL_NODE_IS_TAIL(base, (*node))){ //easy scenario
		base->tail = pnext;
		free(*pdel);
		*pdel = NULL;
	
	} else { 
	
		//find previous node 
		SLNode * prev = findPrevNode(base, *node);
		if(prev == NULL) { //probably passed in wrong base
			return NODE_NOT_FOUND;
		}
		
		prev->next = (*node)->next; //either next node, or NULL
		
		if (SL_NODE_IS_HEAD(base, *node)) {
			base -> head = prev;
		}
		
		free(*node);
		*node = NULL;	
	}

	return 0;
}

inline SLNode * findPrevNodeSafe(struct SLBase _ * base, SLNode * node){
	
	SLNode * prev = SLBase->tail;
	SLNode * next;
	
	if(prev == node){
		return NULL; // node was tail
	}
	
	while((prev != NULL) && ((next = prev->next) != node)){ //short-circuit if NULL
		prev = next;
	}
	
	/*
	while((next != NULL) && (next != node)){
		prev = next;
		next = next->next;
	}	
	*/
	
	return prev; //null if nothing found
}

inline SLNode * findPrevNodeUnsafe(struct SLBase _ * base, SLNode * node){
	
	//unsafe function that doesn't error check for tail == node
	
	SLNode * prev = SLBase->tail;
	while((prev != NULL) && (prev->next != node)){ //short-circuit if NULL
		prev = prev->next;
	}
	
	return prev;
}


	
SLNode * slNodePushHead(struct SLBase_ * base, void * data){

	SLNode * newhead = newSLNode();
	SLNode * oldhead = base->head;
	
	newhead->data = data;
	newhead->next = NULL;
	
	oldhead->next = newhead;
	base->head = newhead;

	return newhead;
}

SLNode * slNodePushTail(struct SLBase_ * base, void * data){
	
	SLNode * newtail = emptySLNode();
	
	newtail->data = data;
	newtail->next = oldtail;
	
	base->tail = newtail;
	
	return newtail;
}

SLNode * newSlNode(void * data){

	SLNode * new = malloc(sizeof(SLNode));
	
	new -> data = data;
	new-> next = NULL;
	return new;
}
	
SLNode * emptySLNode(void){

	SLNode * newnode = malloc(sizeof(SLNode));
	
	newnode->data = NULL;
	newnode->next = NULL;
	
	return newnode;
}
	
	
	
	
	
	