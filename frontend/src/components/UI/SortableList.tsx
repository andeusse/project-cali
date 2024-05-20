import React from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { Box } from '@mui/material';
import { SortableItemParameter } from '../../types/scenarios/common';

type Props = {
  list: SortableItemParameter[];
  setList: React.Dispatch<React.SetStateAction<SortableItemParameter[]>>;
  reorder: (
    list: SortableItemParameter[],
    startIndex: number,
    endIndex: number
  ) => SortableItemParameter[];
};

const SortableList = (props: Props) => {
  const { list, setList, reorder } = props;

  const handleDragEnd = (result: any) => {
    const { destination, source } = result;
    if (!destination) return;
    if (
      source.index === destination.index &&
      source.droppableId === destination.droppableId
    )
      return;
    setList((prevTasks) => reorder(prevTasks, source.index, destination.index));
  };

  return (
    <Box sx={{ border: 2 }}>
      <DragDropContext onDragEnd={handleDragEnd}>
        <Droppable droppableId="list">
          {(droppableProvided) => (
            <div
              ref={droppableProvided.innerRef}
              {...droppableProvided.droppableProps}
            >
              {list.map((item, index) => (
                <Draggable
                  key={item.id}
                  index={index}
                  draggableId={`${item.id}`}
                >
                  {(draggableProvided) => (
                    <article
                      ref={draggableProvided.innerRef}
                      {...draggableProvided.dragHandleProps}
                      {...draggableProvided.draggableProps}
                    >
                      <Box
                        sx={{
                          border: 1,
                          padding: '10px',
                        }}
                      >
                        {`${index + 1}. ${item.name}`}
                      </Box>
                    </article>
                  )}
                </Draggable>
              ))}

              {droppableProvided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </Box>
  );
};

export default SortableList;
