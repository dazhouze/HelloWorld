#include<stdio.h>
#include<string.h>

#define HASHSIZE 101

static struct nlist *hashtab[HASHSIZE];
struct nlist *lookup(char *);
char *strdup(char *);

struct nlist {
    struct nlist *next;
    char *name;//key
    char *defn;//value
}


unsigned hash(char *s)
{
    unsigned hashval;
    for (hashval = 0; *s != '\0'; s++)
        hashval = *s + 31 * hashval;
    return hashval % HASHSIZE;
}

struct nlist *lookup(char *s)
{
    struct nlist *np;
    for (np = hashtab[hash(s)]; np != NULL; np = np->next)
        if (strcmp(s, np->name) == 0)
            return np;
    return NULL;
}

char *strdup(char *s)
{
    char *p;
    p = (char *) malloc(strlen(s)+1);
    if (p != NULL)
        strcpy(p,s);
    return p;
}

struct nlist *install(char *name, char *defn)
{
    struct nlist *np;
    unsigned hashval;
    if ((np = lookup(name)) == NULL0i){
        np  = (struct nlist *) malloc(sizeof(*np));
        if (np == NULL || (np->name = strdup(name)) == NULL)
            return NULL;
        hashval = hash(name);
        np->next = hashtab[hashval];
    }else
        free((void *) np->defn);
    if ((np->defn = strdup(defn)) == NULL)
        return NULL;
    return np;
    }
}
main{}
