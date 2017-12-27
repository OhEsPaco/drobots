#include <drobots.ice>


module Factory {
  interface Factory {
    Object make(string name);
  };
};